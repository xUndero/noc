# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# CLI FSM
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import socket
import re
import functools
import datetime
from functools import reduce
import sys
from threading import Lock

# Third-party modules
import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.concurrent
import six

# NOC modules
from noc.core.log import PrefixLoggerAdapter
from noc.core.text import replace_re_group
from .error import (
    CLIError,
    CLIAuthFailed,
    CLINoSuperCommand,
    CLILowPrivileges,
    CLIConnectionRefused,
)
from noc.config import config
from noc.core.span import Span
from noc.core.perf import metrics


class CLI(object):
    name = "cli"
    default_port = None
    iostream_class = None
    BUFFER_SIZE = config.activator.buffer_size
    MATCH_TAIL = 256
    # Buffer to check missed ECMA control characters
    MATCH_MISSED_CONTROL_TAIL = 8
    # Retries on immediate disconnect
    CONNECT_RETRIES = config.activator.connect_retries
    # Timeout after immediate disconnect
    CONNECT_TIMEOUT = config.activator.connect_timeout
    # compiled capabilities
    HAS_TCP_KEEPALIVE = hasattr(socket, "SO_KEEPALIVE")
    HAS_TCP_KEEPIDLE = hasattr(socket, "TCP_KEEPIDLE")
    HAS_TCP_KEEPINTVL = hasattr(socket, "TCP_KEEPINTVL")
    HAS_TCP_KEEPCNT = hasattr(socket, "TCP_KEEPCNT")
    HAS_TCP_NODELAY = hasattr(socket, "TCP_NODELAY")
    # Time until sending first keepalive probe
    KEEP_IDLE = 10
    # Keepalive packets interval
    KEEP_INTVL = 10
    # Terminate connection after N keepalive failures
    KEEP_CNT = 3
    SYNTAX_ERROR_CODE = "+@@@NOC:SYNTAXERROR@@@+"

    class InvalidPagerPattern(Exception):
        pass

    def __init__(self, script, tos=None):
        self.script = script
        self.profile = script.profile
        self.logger = PrefixLoggerAdapter(self.script.logger, self.name)
        self.iostream = None
        self.motd = ""
        self.ioloop = None
        self.command = None
        self.prompt_stack = []
        self.patterns = self.profile.patterns.copy()
        self.buffer = ""
        self.is_started = False
        self.result = None
        self.error = None
        self.pattern_table = None
        self.collected_data = []
        self.tos = tos
        self.current_timeout = None
        self.is_closed = False
        self.close_timeout = None
        self.close_timeout_lock = Lock()
        self.setup_complete = False
        self.to_raise_privileges = script.credentials.get("raise_privileges", True)
        self.state = "start"
        # State retries
        self.super_password_retries = self.profile.cli_retries_super_password

    def close(self):
        self.script.close_current_session()
        self.close_iostream()
        if self.ioloop:
            self.logger.debug("Closing IOLoop")
            self.ioloop.close(all_fds=True)
            self.ioloop = None
        self.is_closed = True

    def close_iostream(self):
        if self.iostream:
            self.logger.debug("Closing IOStream")
            self.iostream.close()
            self.iostream = None

    def set_state(self, state):
        self.logger.debug("Changing state to <%s>", state)
        self.state = state

    def maybe_close(self):
        with self.close_timeout_lock:
            if not self.close_timeout:
                return  # Race with execute(), no need to close
            if self.ioloop:
                self.ioloop.remove_timeout(self.close_timeout)
            self.close_timeout = None
            self.close()

    def reset_close_timeout(self):
        with self.close_timeout_lock:
            if self.close_timeout:
                self.logger.debug("Removing close timeout")
                self.ioloop.remove_timeout(self.close_timeout)
                self.close_timeout = None

    def deferred_close(self, session_timeout):
        if self.is_closed or not self.iostream:
            return
        self.logger.debug("Setting close timeout to %ss", session_timeout)
        # Cannot call call_later directly due to
        # thread-safety problems
        # See tornado issue #1773
        tornado.ioloop.IOLoop.instance().add_callback(self._set_close_timeout, session_timeout)

    def _set_close_timeout(self, session_timeout):
        """
        Wrapper to deal with IOLoop.add_timeout thread safety problem
        :param session_timeout:
        :return:
        """
        with self.close_timeout_lock:
            self.close_timeout = tornado.ioloop.IOLoop.instance().call_later(
                session_timeout, self.maybe_close
            )

    def create_iostream(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.tos:
            self.logger.debug("Setting IP ToS to %d", self.tos)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, self.tos)
        if self.HAS_TCP_NODELAY:
            self.logger.info("Setting TCP NODELAY")
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if self.HAS_TCP_KEEPALIVE:
            self.logger.info("Settings KEEPALIVE")
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if self.HAS_TCP_KEEPIDLE:
                self.logger.info("Setting TCP KEEPIDLE to %d", self.KEEP_IDLE)
                s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, self.KEEP_IDLE)
            if self.HAS_TCP_KEEPINTVL:
                self.logger.info("Setting TCP KEEPINTVL to %d", self.KEEP_INTVL)
                s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, self.KEEP_INTVL)
            if self.HAS_TCP_KEEPCNT:
                self.logger.info("Setting TCP KEEPCNT to %d", self.KEEP_CNT)
                s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, self.KEEP_CNT)
        return self.iostream_class(s, self)

    def set_timeout(self, timeout):
        if timeout:
            self.logger.debug("Setting timeout: %ss", timeout)
            self.current_timeout = datetime.timedelta(seconds=timeout)
        else:
            if self.current_timeout:
                self.logger.debug("Resetting timeouts")
            self.current_timeout = None

    def run_sync(self, func, *args, **kwargs):
        """
        Simplified implementation of IOLoop.run_sync
        to distinguish real TimeoutErrors from incomplete futures
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        future_cell = [None]

        def run():
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    result = tornado.gen.convert_yielded(result)
                future_cell[0] = result
            except Exception:
                future_cell[0] = tornado.concurrent.TracebackFuture()
                future_cell[0].set_exc_info(sys.exc_info())
            self.ioloop.add_future(future_cell[0], lambda future: self.ioloop.stop())

        self.ioloop.add_callback(run)
        self.ioloop.start()
        if not future_cell[0].done():
            self.logger.info("Incomplete feature left. Restarting IOStream")
            self.close_iostream()
            # Retain cryptic message as is,
            # Mark feature as done
            future_cell[0].set_exception(
                tornado.gen.TimeoutError("Operation timed out after %s seconds" % None)
            )
        return future_cell[0].result()

    def execute(
        self,
        cmd,
        obj_parser=None,
        cmd_next=None,
        cmd_stop=None,
        ignore_errors=False,
        allow_empty_response=True,
    ):
        self.reset_close_timeout()
        self.buffer = ""
        self.command = cmd
        self.error = None
        self.ignore_errors = ignore_errors
        self.allow_empty_response = allow_empty_response
        if not self.ioloop:
            self.logger.debug("Creating IOLoop")
            self.ioloop = tornado.ioloop.IOLoop()
        if obj_parser:
            parser = functools.partial(self.parse_object_stream, obj_parser, cmd_next, cmd_stop)
        else:
            parser = self.read_until_prompt
        with Span(
            server=self.script.credentials.get("address"), service=self.name, in_label=cmd
        ) as s:
            self.run_sync(self.submit, parser)
            if self.error:
                if s:
                    s.error_text = str(self.error)
                raise self.error
            else:
                return self.result

    @tornado.gen.coroutine
    def submit(self, parser=None):
        # Create iostream and connect, when necessary
        if not self.iostream:
            self.iostream = self.create_iostream()
            address = (
                self.script.credentials.get("address"),
                self.script.credentials.get("cli_port", self.default_port),
            )
            self.logger.debug("Connecting %s", address)
            try:
                metrics["cli_connection", ("proto", self.name)] += 1
                yield self.iostream.connect(address)
                metrics["cli_connection_success", ("proto", self.name)] += 1
            except tornado.iostream.StreamClosedError:
                self.logger.debug("Connection refused")
                metrics["cli_connection_refused", ("proto", self.name)] += 1
                self.error = CLIConnectionRefused("Connection refused")
                raise tornado.gen.Return(None)
            self.logger.debug("Connected")
            yield self.iostream.startup()
        # Perform all necessary login procedures
        metrics["cli_commands", ("proto", self.name)] += 1
        if not self.is_started:
            yield self.on_start()
            self.motd = yield self.read_until_prompt()
            self.script.set_motd(self.motd)
            self.is_started = True
        # Send command
        # @todo: encode to object's encoding
        if self.profile.batch_send_multiline or self.profile.command_submit not in self.command:
            yield self.send(self.command)
        else:
            # Send multiline commands line-by-line
            for cmd in self.command.split(self.profile.command_submit):
                # Send line
                yield self.send(cmd + self.profile.command_submit)
                # @todo: Await response
        parser = parser or self.read_until_prompt
        self.result = yield parser()
        self.logger.debug("Command: %s\n%s", self.command.strip(), self.result)
        if (
            self.profile.rx_pattern_syntax_error
            and not self.ignore_errors
            and parser == self.read_until_prompt
            and (
                self.profile.rx_pattern_syntax_error.search(self.result)
                or self.result == self.SYNTAX_ERROR_CODE
            )
        ):
            error_text = self.result
            if self.profile.send_on_syntax_error and self.name != "beef_cli":
                self.allow_empty_response = True
                yield self.on_error_sequence(
                    self.profile.send_on_syntax_error, self.command, error_text
                )
            self.error = self.script.CLISyntaxError(error_text)
            self.result = None
        raise tornado.gen.Return(self.result)

    def cleaned_input(self, s):
        """
        Clean up received input and wipe out control sequences
        and rogue chars
        """
        # Wipe out rogue chars
        if self.profile.rogue_chars:
            for rc in self.profile.rogue_chars:
                try:
                    s = rc.sub("", s)  # rc is compiled regular expression
                except AttributeError:
                    s = s.replace(rc, "")  # rc is a string
        # Clean control sequences
        return self.profile.cleaned_input(s)

    @tornado.gen.coroutine
    def send(self, cmd):
        # @todo: Apply encoding
        cmd = str(cmd)
        self.logger.debug("Send: %r", cmd)
        yield self.iostream.write(cmd)

    @tornado.gen.coroutine
    def read_until_prompt(self):
        connect_retries = self.CONNECT_RETRIES
        while True:
            try:
                metrics["cli_reads", ("proto", self.name)] += 1
                f = self.iostream.read_bytes(self.BUFFER_SIZE, partial=True)
                if self.current_timeout:
                    r = yield tornado.gen.with_timeout(self.current_timeout, f)
                else:
                    r = yield f
                if r == self.SYNTAX_ERROR_CODE:
                    metrics["cli_syntax_errors", ("proto", self.name)] += 1
                    raise tornado.gen.Return(self.SYNTAX_ERROR_CODE)
                metrics["cli_read_bytes", ("proto", self.name)] += len(r)
                if self.script.to_track:
                    self.script.push_cli_tracking(r, self.state)
            except tornado.iostream.StreamClosedError:
                # Check if remote end closes connection just
                # after connection established
                if not self.is_started and connect_retries:
                    self.logger.info(
                        "Connection reset. %d retries left. Waiting %d seconds",
                        connect_retries,
                        self.CONNECT_TIMEOUT,
                    )
                    while connect_retries:
                        yield tornado.gen.sleep(self.CONNECT_TIMEOUT)
                        connect_retries -= 1
                        self.iostream = self.create_iostream()
                        address = (
                            self.script.credentials.get("address"),
                            self.script.credentials.get("cli_port", self.default_port),
                        )
                        self.logger.debug("Connecting %s", address)
                        try:
                            yield self.iostream.connect(address)
                            yield self.iostream.startup()
                            break
                        except tornado.iostream.StreamClosedError:
                            if not connect_retries:
                                raise tornado.iostream.StreamClosedError()
                    continue
                else:
                    raise tornado.iostream.StreamClosedError()
            except tornado.gen.TimeoutError:
                self.logger.info("Timeout error")
                metrics["cli_timeouts", ("proto", self.name)] += 1
                # IOStream must be closed to prevent hanging read callbacks
                self.close_iostream()
                raise tornado.gen.TimeoutError("Timeout")
            self.logger.debug("Received: %r", r)
            # Clean input
            if self.buffer.find("\x1b", -self.MATCH_MISSED_CONTROL_TAIL) != -1:
                self.buffer = self.cleaned_input(self.buffer + r)
            else:
                self.buffer += self.cleaned_input(r)
            # Try to find matched pattern
            offset = max(0, len(self.buffer) - self.MATCH_TAIL)
            for rx, handler in six.iteritems(self.pattern_table):
                match = rx.search(self.buffer, offset)
                if match:
                    self.logger.debug("Match: %s", rx.pattern)
                    matched = self.buffer[: match.start()]
                    self.buffer = self.buffer[match.end() :]
                    if isinstance(handler, tuple):
                        metrics["cli_state", ("state", handler[0].__name__)] += 1
                        r = yield handler[0](matched, match, *handler[1:])
                    else:
                        metrics["cli_state", ("state", handler.__name__)] += 1
                        r = yield handler(matched, match)
                    if r is not None:
                        raise tornado.gen.Return(r)
                    else:
                        break  # This state is processed

    @tornado.gen.coroutine
    def parse_object_stream(self, parser=None, cmd_next=None, cmd_stop=None):
        """
        :param cmd:
        :param command_submit:
        :param parser: callable accepting buffer and returning
                       (key, data, rest) or None.
                       key - string with object distinguisher
                       data - dict containing attributes
                       rest -- unparsed rest of string
        :param cmd_next: Sequence to go to the next page
        :param cmd_stop: Sequence to stop
        :return:
        """
        self.logger.debug("Parsing object stream")
        objects = []
        seen = set()
        buffer = ""
        repeats = 0
        r_key = None
        stop_sent = False
        done = False
        while not done:
            r = yield self.iostream.read_bytes(self.BUFFER_SIZE, partial=True)
            if self.script.to_track:
                self.script.push_cli_tracking(r, self.state)
            self.logger.debug("Received: %r", r)
            buffer = self.cleaned_input(buffer + r)
            # Check for syntax error
            if (
                self.profile.rx_pattern_syntax_error
                and not self.ignore_errors
                and self.profile.rx_pattern_syntax_error.search(self.buffer)
            ):
                error_text = self.buffer
                if self.profile.send_on_syntax_error:
                    yield self.on_error_sequence(
                        self.profile.send_on_syntax_error, self.command, error_text
                    )
                self.error = self.script.CLISyntaxError(error_text)
                break
            # Then check for operation error
            if (
                self.profile.rx_pattern_operation_error
                and self.profile.rx_pattern_operation_error.search(self.buffer)
            ):
                self.error = self.script.CLIOperationError(self.buffer)
                break
            # Parse all possible objects
            while buffer:
                pr = parser(buffer)
                if not pr:
                    break  # No new objects
                key, obj, buffer = pr
                if key not in seen:
                    seen.add(key)
                    objects += [obj]
                    repeats = 0
                    r_key = None
                elif r_key:
                    if r_key == key:
                        repeats += 1
                        if repeats >= 3 and cmd_stop and not stop_sent:
                            # Stop loop at final page
                            # After 3 repeats
                            self.logger.debug("Stopping stream. Sending %r" % cmd_stop)
                            self.send(cmd_stop)
                            stop_sent = True
                else:
                    r_key = key
                    if cmd_next:
                        self.logger.debug("Next screen. Sending %r" % cmd_next)
                        self.send(cmd_next)
            # Check for prompt
            for rx, handler in six.iteritems(self.pattern_table):
                offset = max(0, len(buffer) - self.MATCH_TAIL)
                match = rx.search(buffer, offset)
                if match:
                    self.logger.debug("Match: %s", rx.pattern)
                    matched = buffer[: match.start()]
                    buffer = self.buffer[match.end() :]
                    r = handler(matched, match)
                    if r is not None:
                        self.logger.debug("Prompt matched")
                        done = True
                        break
        raise tornado.gen.Return(objects)

    def send_pager_reply(self, data, match):
        """
        Send proper pager reply
        """
        pg = match.group(0)
        for p, c in self.patterns["more_patterns_commands"]:
            if p.search(pg):
                self.collected_data += [data]
                self.send(c)
                return
        raise self.InvalidPagerPattern(pg)

    def expect(self, patterns, timeout=None):
        """
        Send command if not none and set reply patterns
        """
        self.pattern_table = {}
        for pattern_name in patterns:
            rx = self.patterns.get(pattern_name)
            if not rx:
                continue
            self.pattern_table[rx] = patterns[pattern_name]
        self.set_timeout(timeout)

    @tornado.gen.coroutine
    def on_start(self, data=None, match=None):
        self.set_state("start")
        if self.profile.setup_sequence and not self.setup_complete:
            self.expect({"setup": self.on_setup_sequence}, self.profile.cli_timeout_setup)
        else:
            self.expect(
                {
                    "username": self.on_username,
                    "password": self.on_password,
                    "unprivileged_prompt": self.on_unprivileged_prompt,
                    "prompt": self.on_prompt,
                    "pager": self.send_pager_reply,
                },
                self.profile.cli_timeout_start,
            )

    @tornado.gen.coroutine
    def on_username(self, data, match):
        self.set_state("username")
        self.send(
            (self.script.credentials.get("user", "") or "") + (self.profile.username_submit or "\n")
        )
        self.expect(
            {
                "username": (self.on_failure, CLIAuthFailed),
                "password": self.on_password,
                "unprivileged_prompt": self.on_unprivileged_prompt,
                "prompt": self.on_prompt,
            },
            self.profile.cli_timeout_user,
        )

    @tornado.gen.coroutine
    def on_password(self, data, match):
        self.set_state("password")
        self.send(
            (self.script.credentials.get("password", "") or "")
            + (self.profile.password_submit or "\n")
        )
        self.expect(
            {
                "username": (self.on_failure, CLIAuthFailed),
                "password": (self.on_failure, CLIAuthFailed),
                "unprivileged_prompt": self.on_unprivileged_prompt,
                "super_password": self.on_super_password,
                "prompt": self.on_prompt,
                "pager": self.send_pager_reply,
            },
            self.profile.cli_timeout_password,
        )

    @tornado.gen.coroutine
    def on_unprivileged_prompt(self, data, match):
        self.set_state("unprivileged_prompt")
        if self.to_raise_privileges:
            # Start privilege raising sequence
            if not self.profile.command_super:
                self.on_failure(data, match, CLINoSuperCommand)
            self.send(self.profile.command_super + (self.profile.command_submit or "\n"))
            # Do not remove `pager` section
            # It fixes this situation on Huawei MA5300:
            # xxx>enable
            # { <cr>|level-value<U><1,15> }:
            # xxx#
            self.expect(
                {
                    "username": self.on_super_username,
                    "password": self.on_super_password,
                    "prompt": self.on_prompt,
                    "pager": self.send_pager_reply,
                },
                self.profile.cli_timeout_super,
            )
        else:
            # Do not raise privileges
            # Use unprivileged prompt as primary prompt
            self.patterns["prompt"] = self.patterns["unprivileged_prompt"]
            return self.on_prompt(data, match)

    @tornado.gen.coroutine
    def on_failure(self, data, match, error_cls=None):
        self.set_state("failure")
        error_cls = error_cls or CLIError
        raise error_cls(self.buffer or data or None)

    @tornado.gen.coroutine
    def on_prompt(self, data, match):
        self.set_state("prompt")
        if not self.allow_empty_response:
            s_data = data.strip()
            if not s_data or s_data == self.command.strip():
                return None
        if not self.is_started:
            self.resolve_pattern_prompt(match)
        d = "".join(self.collected_data + [data])
        self.collected_data = []
        self.expect({"prompt": self.on_prompt, "pager": self.send_pager_reply})
        return d

    @tornado.gen.coroutine
    def on_super_username(self, data, match):
        self.set_state("super_username")
        self.send(
            (self.script.credentials.get("user", "") or "") + (self.profile.username_submit or "\n")
        )
        self.expect(
            {
                "username": (self.on_failure, CLILowPrivileges),
                "password": self.on_super_password,
                "unprivileged_prompt": self.on_unprivileged_prompt,
                "prompt": self.on_prompt,
                "pager": self.send_pager_reply,
            },
            self.profile.cli_timeout_user,
        )

    @tornado.gen.coroutine
    def on_super_password(self, data, match):
        self.set_state("super_password")
        self.send(
            (self.script.credentials.get("super_password", "") or "")
            + (self.profile.username_submit or "\n")
        )
        if self.super_password_retries > 1:
            unprivileged_handler = self.on_unprivileged_prompt
            self.super_password_retries -= 1
        else:
            unprivileged_handler = (self.on_failure, CLILowPrivileges)
        self.expect(
            {
                "prompt": self.on_prompt,
                "password": (self.on_failure, CLILowPrivileges),
                "super_password": (self.on_failure, CLILowPrivileges),
                "pager": self.send_pager_reply,
                "unprivileged_prompt": unprivileged_handler,
            },
            self.profile.cli_timeout_password,
        )

    @tornado.gen.coroutine
    def on_setup_sequence(self, data, match):
        self.set_state("setup")
        self.logger.debug("Performing setup sequence: %s", self.profile.setup_sequence)
        lseq = len(self.profile.setup_sequence)
        for i, c in enumerate(self.profile.setup_sequence):
            if isinstance(c, six.integer_types) or isinstance(c, float):
                yield tornado.gen.sleep(c)
                continue
            cmd = c % self.script.credentials
            yield self.send(cmd)
            # Waiting for response and drop it
            if i < lseq - 1:
                resp = yield tornado.gen.with_timeout(
                    self.ioloop.time() + 30,
                    future=self.iostream.read_bytes(4096, partial=True),
                    io_loop=self.ioloop,
                )
                if self.script.to_track:
                    self.script.push_cli_tracking(resp, self.state)
                self.logger.debug("Receiving: %r", resp)
        self.logger.debug("Setup sequence complete")
        self.setup_complete = True
        yield self.on_start(data, match)

    def resolve_pattern_prompt(self, match):
        """
        Resolve adaptive pattern prompt
        """
        old_pattern_prompt = self.patterns["prompt"].pattern
        pattern_prompt = old_pattern_prompt
        sl = self.profile.can_strip_hostname_to
        for k, v in six.iteritems(match.groupdict()):
            if v:
                if k == "hostname" and sl and len(v) > sl:
                    ss = list(reversed(v[sl:]))
                    v = re.escape(v[:sl]) + reduce(
                        lambda x, y: "(?:%s%s)?" % (re.escape(y), x),
                        ss[1:],
                        "(?:%s)?" % re.escape(ss[0]),
                    )
                else:
                    v = re.escape(v)
                pattern_prompt = replace_re_group(pattern_prompt, "(?P<%s>" % k, v)
                pattern_prompt = replace_re_group(pattern_prompt, "(?P=%s" % k, v)
            else:
                self.logger.error("Invalid prompt pattern")
        if old_pattern_prompt != pattern_prompt:
            self.logger.debug("Refining pattern prompt to %r", pattern_prompt)
        self.patterns["prompt"] = re.compile(pattern_prompt, re.DOTALL | re.MULTILINE)

    def push_prompt_pattern(self, pattern):
        """
        Override prompt pattern
        """
        self.logger.debug("New prompt pattern: %s", pattern)
        self.prompt_stack += [self.patterns["prompt"]]
        self.patterns["prompt"] = re.compile(pattern, re.DOTALL | re.MULTILINE)
        self.pattern_table[self.patterns["prompt"]] = self.on_prompt

    def pop_prompt_pattern(self):
        """
        Restore prompt pattern
        """
        self.logger.debug("Restore prompt pattern")
        pattern = self.prompt_stack.pop(-1)
        self.patterns["prompt"] = pattern
        self.pattern_table[self.patterns["prompt"]] = self.on_prompt

    def get_motd(self):
        """
        Return collected message of the day
        """
        return self.motd

    def set_script(self, script):
        self.script = script
        self.logger = PrefixLoggerAdapter(self.script.logger, self.name)
        self.reset_close_timeout()
        if self.motd:
            self.script.set_motd(self.motd)

    def setup_session(self):
        if self.profile.setup_session:
            self.logger.debug("Setup session")
            self.profile.setup_session(self.script)

    def shutdown_session(self):
        if self.profile.shutdown_session:
            self.logger.debug("Shutdown session")
            self.profile.shutdown_session(self.script)

    @tornado.gen.coroutine
    def on_error_sequence(self, seq, command, error_text):
        """
        Process error sequence
        :param seq:
        :param command:
        :param error_text:
        :return:
        """
        if isinstance(seq, six.string_types):
            self.logger.debug("Recovering from error. Sending %r", seq)
            yield self.iostream.write(seq)
        elif callable(seq):
            if tornado.gen.is_coroutine_function(seq):
                # Yield coroutine
                yield seq(self, command, error_text)
            else:
                seq = seq(self, command, error_text)
                yield self.iostream.write(seq)
