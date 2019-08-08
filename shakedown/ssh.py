# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import multiprocessing as mp
import signal
import pexpect
import re
import time

SSH_INIT_RE = ["(?i)are you sure you want to continue connecting",
               r"(?i)((\w+\@)?[\w\-]+\'s)? ?password:"]

PROMPT_RE = [
    # Matches on:
    # cs-spine-2a......14:08:54#
    # cs-spine-2a[14:08:54]#
    # cs-spine-2a>
    # cs-spine-2a#
    # cs-spine-2a(s1)#
    # cs-spine-2a(s1)(config)#
    # cs-spine-2b(vrf:management)(config)#
    # cs-spine-2b(s1)(vrf:management)(config)#
    r"[\w+\-\.:\/\[\]]+(?:\([^\)]+\)){,3}(?:>|#) ?$",
    # Matches on:
    # [admin@cs-spine-2a /]$
    # [admin@cs-spine-2a local]$
    # [admin@cs-spine-2a ~]$
    r"\[\w+\@[\w\-\.]+(?: [^\]])\] ?[>#\$] ?$",
    # Matches on:
    # -bash-4.1#
    # #
    r"\-?(?:bash)?(?:\-\d\.\d)? ?[>#\$] ?$"
]

ANSI_ESCAPE_RE = r'\x1B\[[0-?]*[ -/]*[@-~]'

class SshException(Exception):
    pass

class SshSessionClosedException(SshException):
    pass

class SshCopyException(SshException):
    pass

def _decode(text):
    """cleanup responses"""
    return re.sub(ANSI_ESCAPE_RE, "", text.decode("utf-8")).rstrip()

class Session:

    def __init__(self):
        self.hostaddr = None
        self.auth = ("admin", "")

        # pexpect child object
        self.child = None

        self.prompt = None
        self.motd = None
        self.banner = None

        self._opened = False

        # spawn cmd
        self._spawn_cmd = "ssh -l {username} {host}"

    def __enter__(self, *args, **kwargs):
        #self.spawn(self.spawn_cmd)
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @property
    def opened(self):
        if self._opened:
            return True

    @property
    def alive(self):
        return self.child.isalive()

    @property
    def closed(self):
        return not self.opened

    def _decode(self, text):
        """cleanup responses"""
        return re.sub(ANSI_ESCAPE_RE, "", text.decode("utf-8")).rstrip()

    def close(self):
        if self.opened:
            # safety check so we don't infinitely loop...
            max_retries = 5
            retries = 0
            while self.child.isalive():
                if retries > 0:
                    time.sleep(1)

                if retries >= max_retries:
                    raise SshException("Max retries reached, session did not close.")

                self.child.close(force=True)
                retries += 1

        self._opened = False

    def send(self, line, prompt=None, input=None, timeout=30):
        if not self.opened:
            self.reopen()

        self.child.sendline(line)

        if prompt:
            index = self.child.expect([prompt], timeout=timeout)
            if index == 0:
                self.child.sendline(input)

        try:
            self.child.expect(PROMPT_RE, timeout=timeout)
        except pexpect.EOF:
            raise SshSessionClosedException("SSH connection has gone away")

        self.prompt = _decode(self.child.after)

        # decode and delete the echoed command from the output
        return "\n".join(_decode(self.child.before).splitlines()[1:])

    def reopen(self):
        if not self.hostaddr:
            raise ValueError("Session has never been opened")

        self.close()
        self.open(self.hostaddr, self.auth)

    def open(self, hostaddr, auth=None):
        """spawn a new SSH session"""

        if not auth:
            auth = self.auth

        username, password = auth
        cmd = self._spawn_cmd.format(
            username=username,
            host=hostaddr
        )

        self.child = pexpect.spawn(cmd)

        index = self.child.expect(SSH_INIT_RE + PROMPT_RE)
        self.banner = _decode(self.child.before)

        if index == 0:
            self.child.sendline("yes")
            index = self.child.expect(SSH_INIT_RE)
            self.motd = _decode(self.child.before)

        if index == 1:
            self.child.sendline(password)
            # prepend the prompts to ensure the index is 2
            _prompt_re = [r"$^"] * 2 + PROMPT_RE + \
                [r"(?i)permission denied", pexpect.EOF]
            index = self.child.expect(_prompt_re)

            if index == len(_prompt_re) - 2:
                raise SshException("Login failed: %s" % _prompt_re[index])
            elif index <= len(PROMPT_RE) - 1:
                self.prompt = _decode(self.child.after) #self.child.after.decode("utf-8")

            self.motd = _decode(self.child.before)

        if index > 1:
            self.motd = _decode(self.child.before)

        self._opened = True

        # save args so the connection can be re-opened if needed
        self.hostaddr = hostaddr
        self.auth = auth

        # if we are in CLI turn off paging
        if index == 2:
            self.send("terminal length 0")
            self.send("terminal width 32767")

def session(*args, **kwargs):
    sess = Session()
    sess.open(*args, **kwargs)
    return sess

def copy(source, destination, password=""):
    """Copy a file from or to a remote destination"""

    #user, password = auth
    cmd = "scp -q %s %s" % (source, destination)

    _init_re = SSH_INIT_RE + [pexpect.EOF]

    child = pexpect.spawn(cmd)

    index = child.expect(_init_re)

    if index == 0:
        child.sendline("yes")
        index = child.expect(_init_re)

    if index == 1:
        child.sendline(password)

    child.close()

    if child.exitstatus > 0:
        raise SshCopyException(_decode(child.before))


# def _prep_worker():
#     """Tell workers to ignore interrupts"""
#     signal.signal(signal.SIGINT, signal.SIG_IGN)

def _bg_worker(hostaddr, auth, command):
    sess = Session()
    sess.open(hostaddr, auth)

    response = sess.send(command)

    sess.close()

    return response

class Background(object):

    def __init__(self, hostaddr, auth, command, callback=None, delay=0, **kwargs):

        # delay the return of start- give slower sessions time to initialize
        self._delay = delay

        self._callback = callback

        # commands to be executed on each session
        self._command = command

        self._hostaddr = hostaddr
        self._auth = auth

        self._results = []

        self._pool = mp.Pool()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        self.join()
        pass

    def __iter__(self):
        for item in self._results:
            yield item.get()

    @property
    def delay(self):
        return self._delay

    @property
    def hostaddr(self):
        return self._hostaddr

    @property
    def results(self):
        return self._results

    def start(self):

        args = (self._hostaddr, self._auth, self._command)
        result = self._pool.apply_async(_bg_worker, args,
                                        callback=self._callback)
        self._results.append(result)

        time.sleep(self._delay)

    def join(self):
        self._pool.join()

    def close(self):
        self._pool.close()

    def kill(self):
        self._pool.terminate()
