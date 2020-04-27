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

ANSI_ESCAPE_RE = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)
#re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]', re.I)

SSH_OPTIONS = [
    "StrictHostKeyChecking=no"
]

class SshException(Exception):
    pass

class SshSessionClosedException(SshException):
    pass

class SshCopyException(SshException):
    pass

class SshTimeoutException(SshException):
    pass

def _decode(text):
    """cleanup responses"""
    decoded = text.decode()
    escaped = ANSI_ESCAPE_RE.sub("", decoded)
    stripped = escaped.rstrip()
    return stripped

class Session:

    def __init__(self):
        self.hostaddr = None

        # default username/password
        self.auth = ("admin", "")

        # pexpect child object
        self._child = None

        self.prompt = None
        self.motd = None
        self.banner = None

        self._opened = False

        # spawn cmd
        self._spawn_cmd = "ssh -l {username} {options} {host}"

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
        return self._child.isalive()

    @property
    def closed(self):
        return not self.opened

    # def _decode(self, text):
    #     """cleanup responses"""
    #     print("DECODING: ", text)
    #     return re.sub(ANSI_ESCAPE_RE, "", text.decode("utf-8")).rstrip()

    def close(self):
        if self.opened:
            # safety check so we don't infinitely loop...
            max_retries = 5
            retries = 0
            while self._child.isalive():
                if retries > 0:
                    time.sleep(1)

                if retries >= max_retries:
                    raise SshException("Max retries reached, session did not close.")

                self._child.close(force=True)
                retries += 1

        self._opened = False

    def send(self, line, prompt=None, input=None, timeout=30):
        if not self.opened:
            self.reopen()

        self._child.sendline(line)

        if prompt:
            index = self._child.expect([prompt], timeout=timeout)
            if index == 0:
                self._child.sendline(input)

        try:
            self._child.expect(PROMPT_RE, timeout=timeout)
        except pexpect.EOF:
            raise SshSessionClosedException("SSH connection has gone away")

        self.prompt = _decode(self._child.after)
        
        # decode and delete the echoed command from the output
        #print("OUT>>>", self._child.before)
        #print("WUT>>>", [_decode(o) for o in self._child.before.splitlines()])
        response = [_decode(o) for o in self._child.before.splitlines()][1:-1]
        return "\n".join(response)

    def reopen(self):
        if not self.hostaddr:
            raise ValueError("Session has never been opened")

        self.close()
        self.open(self.hostaddr, self.auth)

    def open_root(self, hostaddr, password):
        self.open(hostaddr, auth=("root", password))
    
    def open(self, hostaddr, auth=None):
        """spawn a new SSH session"""

        if not auth:
            auth = self.auth

        username, password = auth

        options = " ".join(["-o %s" % o for o in SSH_OPTIONS])
        cmd = self._spawn_cmd.format(
            username=username,
            options=options,
            host=hostaddr
        )

        self._child = pexpect.spawn(cmd)

        index = self._child.expect(SSH_INIT_RE + PROMPT_RE)
        self.banner = _decode(self._child.before)

        if index == 0:
            self._child.sendline("yes")
            index = self._child.expect(SSH_INIT_RE)
            self.motd = _decode(self._child.before)

        if index == 1:
            self._child.sendline(password)
            # prepend the prompts to ensure the index is 2
            _prompt_re = [r"$^"] * 2 + PROMPT_RE + \
                [r"(?i)permission denied", pexpect.EOF]
            index = self._child.expect(_prompt_re)

            if index == len(_prompt_re) - 2:
                raise SshException("Login failed: %s" % _prompt_re[index])
            elif index <= len(PROMPT_RE) - 1:
                self.prompt = _decode(self._child.after)

            self.motd = _decode(self._child.before)

        if index > 1:
            self.motd = _decode(self._child.before)

        self._opened = True

        # save args so the connection can be re-opened if needed
        self.hostaddr = hostaddr
        self.auth = auth

        # if we are in CLI turn off paging
        if index == 2:
            self.send("terminal length 0")
            self.send("terminal width 32767")
        else:
            self.send("export TERM=dumb")

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

def _bg_worker(hostaddr, auth, command):
    sess = Session()
    sess.open(hostaddr, auth)

    try:
        response = sess.send(command)
    except pexpect.exceptions.TIMEOUT as exc:
        raise SshTimeoutException(str(exc))

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
