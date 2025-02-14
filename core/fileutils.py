# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import os
import tempfile
import hashlib
import tarfile
import gzip
import shutil

# Third-party modules
import six

# NOC modules
from noc.core.version import version


def safe_rewrite(path, text, mode=None):
    """
    Create new file filled with "text" safely
    """
    if isinstance(text, unicode):
        text = text.encode("utf-8")
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d)
    b = os.path.basename(path)
    h, p = tempfile.mkstemp(suffix=".tmp", prefix=b, dir=d)
    f = os.fdopen(h, "w")
    f.write(text)
    f.flush()
    f.close()
    if os.path.exists(path):
        os.unlink(path)
    os.link(p, path)
    os.unlink(p)
    if mode:
        os.chmod(path, mode)


def safe_append(path, text):
    """
    Append the text to the end of the file
    """
    if isinstance(text, unicode):
        text = text.encode("utf-8")
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d)
    with open(path, "a") as f:
        f.write(text)


def is_differ(path, content):
    """
    Check file content is differ from string
    """
    if os.path.isfile(path):
        with open(path) as f:
            cs1 = hashlib.sha1(f.read()).digest()
        cs2 = hashlib.sha1(content).digest()
        return cs1 != cs2
    else:
        return True


def rewrite_when_differ(path, content):
    """
    Rewrites file when content is differ
    Returns boolean signalling wherher file was rewritten
    """
    d = is_differ(path, content)
    if d:
        safe_rewrite(path, content)
    return d


def read_file(path):
    """
    Read file and return file's content.
    Return None when file does not exists
    """
    if os.path.isfile(path) and os.access(path, os.R_OK):
        with open(path, "r") as f:
            return f.read()
    else:
        return None


def copy_file(f, t, mode=None):
    """
    Copy File
    """
    d = read_file(f)
    if d is None:
        d = ""
    safe_rewrite(t, d, mode=mode)


def write_tempfile(text):
    """
    Create temporary file, write content and return path
    """
    h, p = tempfile.mkstemp()
    f = os.fdopen(h, "w")
    f.write(text)
    f.close()
    return p


class temporary_file(object):
    """
    Temporary file context manager.
    Writes data to temporary file an returns path.
    Unlinks temporary file on exit
    USAGE:
         with temporary_file("line1\nline2") as p:
             subprocess.Popen(["wc","-l",p])
    """

    def __init__(self, text=""):
        self.text = text

    def __enter__(self):
        self.p = write_tempfile(self.text)
        return self.p

    def __exit__(self, type, value, tb):
        os.unlink(self.p)


def in_dir(file, dir):
    """
    Check file is inside dir
    """
    return os.path.commonprefix([dir, os.path.normpath(file)]) == dir


def urlopen(url, auto_deflate=False):
    """
    urlopen wrapper
    """
    from future.moves.urllib.request import urlopen, Request
    from noc.core.http.proxy import setup_urllib_proxies

    setup_urllib_proxies()

    if url.startswith("http://") or url.startswith("https://"):
        r = Request(url, headers={"User-Agent": "NOC/%s" % version.version.strip()})
    else:
        r = url
    if auto_deflate and url.endswith(".gz"):
        u = urlopen(r)
        f = six.StringIO(u.read())
        return gzip.GzipFile(fileobj=f)
    return urlopen(r)


def search_path(file):
    """
    Search for executable file in $PATH
    :param file: File name
    :return: path or None
    :rtype: str or None
    """
    if os.path.exists(file):
        return file  # Found
    for d in os.environ["PATH"].split(os.pathsep):
        f = os.path.join(d, file)
        if os.path.exists(f):
            return f
    return None


def tail(path, lines):
    """
    Return string containing last lines of file
    :param lines:
    :return:
    """
    with open(path) as f:
        avg = 74
        while True:
            try:
                f.seek(-avg * lines, 2)
            except IOError:
                f.seek(0)
            pos = f.tell()
            ln = f.read().splitlines()
            if len(ln) >= lines or not pos:
                return ln[-lines:]
            avg *= 1.61


def iter_open(path):
    """
    Generator yielding file-like objects from path
    :param path:
    :return:
    """
    if path.endswith("tar.gz") or path.endswith("tgz"):
        tf = tarfile.open(path, "r:gz")
        for name in tf:
            f = tf.extractfile(name)
            yield f
        tf.close()
    elif path.endswith("tar.bz2") or path.endswith("tbz"):
        tf = tarfile.open(path, "r:bz")
        for f in tf:
            yield f
        tf.close()
    elif path.endswith(".gz"):
        f = gzip.open(path, "r")
        yield f
        f.close()
    else:
        f = open(path, "r")
        yield f
        f.close()


def make_persistent(path, tmp_suffix=".tmp"):
    """
    Make file persistent removing `tmp_suffix` suffix

    :param path: File path
    :return: True if file has been moved, false otherwise
    """
    if not path.endswith(tmp_suffix):
        return False
    shutil.move(path, path[: -len(tmp_suffix)])
