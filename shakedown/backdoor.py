# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pexpect
import eapi
import re
import sys
import time
import requests

SSH_INIT_RE = ["(?i)are you sure you want to continue connecting",
               r"(?i)((\w+\@)?\w+\'s)? ?password:"]

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

EAPI_CREDS = ("admin", "")

class BackdoorClosed(Exception): pass


def _send_pass():
    pass

class Backdoor:

    def __init__(self):
        self.host = None
        self.opener = None
        self.child = None

        self.prompt = None
        self.motd = None
        self.banner = None

        self._opened = False
        # default spawn cmd
        self.default_spawn_cmd = "ssh -l {username} {host}"

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

    def close(self):
        if self.opened:
            # safety check so we don't infinitely loop...
            max_retries = 5
            retries = 0
            while self.child.isalive():
                if retries > 0:
                    time.sleep(1)

                if retries >= max_retries:
                    raise ValueError("Max retries reached, session did not close.")

                self.child.close(force=True)
                retries += 1

        self._opened = False

    def install(self, host, password="root", creds=None):
        if not creds:
            creds = EAPI_CREDS

        sess = eapi.Session(host, auth=creds)
        r = sess.send([
            "configure",
            "aaa root secret %s" % password,
            "end"
        ])

    def send(self, line):
        if not self.opened:
            self.reopen()
            #raise BackdoorClosed("Backdoor is not open")

        self.child.sendline(line)
        self.child.expect(PROMPT_RE)

        self.prompt = self.child.after.decode("utf-8")

        return re.sub(ANSI_ESCAPE_RE, "", self.child.before.decode("utf-8"))

    def sendcli(self, line):
        """Wrapper for CLI commands"""
        self.send("Cli -p 15")
        self.send("terminal length 0")
        self.send("terminal width 32767")

        try:
            response = self.send(line)
        except pexpect.EOF:
            self.close()
        else:
            self.send("logout")

        return response

    def reopen(self):
        if not self.opener:
            raise ValueError("Backdoor has not been opened yet")

        self.close()
        self.open(*self.opener[:-1], **self.opener[-1])

    def open(self, host, cmd=None, password="root", creds=None, **kwargs):
        """spawn a new SSH session, and install the backdoor if needed"""

        if not cmd:
            cmd = self.default_spawn_cmd

        cmd = cmd.format(
            username="root",
            host=host,
            **kwargs
        )

        self.child = pexpect.spawn(cmd)

        index = self.child.expect(SSH_INIT_RE)
        self.banner = self.child.before

        if index == 0:
            self.child.sendline("yes")
            index = self.child.expect(SSH_INIT_RE)
            self.motd = self.child.before

        if index == 1:
            self.child.sendline(password)
            _prompt_re = PROMPT_RE + [r"(?i)permission denied", pexpect.EOF]
            index = self.child.expect(_prompt_re)

            if index == len(_prompt_re) - 2:
                self.install(host, creds=creds, password=password)
                self.open(host, cmd, password, **kwargs)
                return
            elif index <= len(PROMPT_RE) - 1:
                self.prompt = self.child.after.decode("utf-8")

            self.motd = self.child.before

        # save args so the connection can be re-opened if needed
        self.opener = (host, cmd, password, creds, kwargs)

        self._opened = True

    def reload(self, save=False, waitfor=0):
        if save:
            self.sendcli(r'Cli -p 15 -c write')

        try:
            self.send(r'echo reload now | Cli -p 15')
            while self.child.isalive():
                pass
        except pexpect.EOF:
            time.sleep(10)

        self._opened = False

        if waitfor > 0:
            t0 = time.time()
            while True:
                try:
                    self.reopen()
                    while True:
                        line = ("echo 'show logging last 120 seconds "
                                "| i SYSTEM_RESTARTED' | Cli -p 15")
                        output = self.send(line)

                        if "System restarted" in output:
                            sys.stdout.write("!\n")
                            sys.stdout.flush()
                            return

                        sys.stdout.write("?")
                        sys.stdout.flush()

                        if int(time.time() - t0) >= waitfor:
                            raise ValueError("Timeout exceeded")

                        time.sleep(5)

                except pexpect.EOF:
                    pass
                except pexpect.TIMEOUT:
                    pass
                except eapi.EapiHttpError:
                    pass

                sys.stdout.write(".")
                sys.stdout.flush()

                if int(time.time() - t0) >= waitfor:
                    raise ValueError("Timeout exceeded")

            time.sleep(10)

    def reload_and_wait(self, save=False):
        return self.reload(save, waitfor=3600)

def execute(host, command, password="root"):
    response = None
    with Backdoor() as bkd:
        sess.open(host, password=password)
        response = bkd.send(command)

    return response

def backdoor(*args, **kwargs):

    return Backdoor(*args, **kwargs)

def copy(host, source_path, destination_path, password="root"):
    bkd = Backdoor()

    try:
        bkd.open(
            host,
            cmd="scp -q {source} {username}@{host}:{destination}",
            password=password,
            source=source_path,
            destination=destination_path
        )
    except pexpect.EOF:
        pass
