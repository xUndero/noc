# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# NSQ Topic Queue
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from collections import deque
from threading import Lock, Condition

# Third-party modules
import six
import ujson


class TopicQueue(object):
    def __init__(self, topic):
        self.topic = topic
        self.lock = Lock()
        self.put_condition = Condition()
        self.queue = deque()  # @todo: maxlen
        self.queue_size = 0
        self.to_shutdown = False

    def put(self, message, fifo=True):
        """
        Put message into queue. Block if queue is full
        
        :param message: Message of any json-serializable type
        :param fifo: Boolean. Append message to the start of queue (LIFO) if False.
            Append message to the end of queue (FIFO) if True.
        :return:
        """
        if not isinstance(message, six.string_types):
            message = ujson.dumps(message)
        with self.lock:
            if self.to_shutdown:
                raise RuntimeError("put() after shutdown")
            if fifo:
                self.queue.append(message)
            else:
                self.queue.appendleft(message)
            self.queue_size += len(message)
        with self.put_condition:
            self.put_condition.notify_all()

    def return_messages(self, messages):
        """
        Return messages to the start of the queue

        :param messages: List of messages
        :return:
        """
        with self.lock:
            if self.to_shutdown:
                raise RuntimeError("return_messages() after shutdown")
            for msg in reversed(messages):
                self.queue.appendleft(msg)

    def iter_get(self, n=1, size=None):
        """
        Get up to `n` items up to `size` size.

        Warning queue will be locked until the end of function call.

        :param n: Amount of items returned
        :param size: None - unlimited, integer - upper size limit
        :return: Yields items
        """
        total = 0
        with self.lock:
            for _i in range(n):
                try:
                    msg = self.queue.popleft()
                    m_size = len(msg)
                    total += m_size
                    if size and total > size:
                        # Size limit exceeded. Return message to queue
                        self.queue.appendleft(msg)
                        break
                    self.queue_size -= m_size
                    yield msg
                except IndexError:
                    break

    def is_empty(self):
        """
        Check if queue is empty

        :return: True if queue is empty, False otherwise
        """
        return not self.queue_size

    def qsize(self):
        """
        Returns amount of messages and size of queue

        :return: messages, total size
        """
        with self.lock:
            return len(self.queue), self.queue_size

    def shutdown(self):
        """
        Begin shutdown sequence. Disable queue writes

        :return:
        """
        if self.to_shutdown:
            raise RuntimeError("Already in shutdown")
        self.to_shutdown = True
        with self.put_condition:
            self.put_condition.notify_all()

    def wait(self, timeout=None):
        """
        Block and wait up to `timeout`

        :param timeout: Wait timeout. No limit if None
        """
        if not self.queue_size:
            return  # Data ready
        with self.put_condition:
            self.put_condition.wait(timeout)
