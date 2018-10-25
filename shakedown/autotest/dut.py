# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pexpect
import tempfile
import os
import functools
import time
import eapi
from shakedown.util import to_list
from shakedown.autotest.constants import SSH_INIT_REGEX, BACKDOOR_CREDENTIALS
from shakedown import backdoor

def _ssh_send_pass(child, password):
    index = child.expect(SSH_INIT_REGEX)
    if index == 0:
        child.sendline("yes")
        index = child.expect(SSH_INIT_REGEX)

    if index == 1:
        child.sendline(password)
        index = child.expect([r'(\$|#) ?', pexpect.EOF])

def _ssh_spawn(host, username, password):
    child = pexpect.spawn("ssh -l %s %s" % (username, host))
    _ssh_send_pass(child, password)

    return child
#
#
# def sshcmd(host, creds, command)

class Dut():
    def __init__(self, sessions, filt):
        self.sessions = sessions
        self.filter = filt

        self.filtered = self.sessions.filter(filt)

    @property
    def host(self):
        return self.filtered[0].endpoint

    @property
    def creds(self):
        return self.filtered[0].creds

    @property
    def protocol(self):
        return self.filtered[0].protocol

    def execute(self, commands, *args, **kwargs):
        commands = to_list(commands)
        return self.sessions.send(self.filter, commands, *args, **kwargs)[0]

    send = execute_until = execute

    def configure(self, commands, *args, **kwargs):
        commands = to_list(commands)
        commands = ["configure"] + commands + ["end"]
        return self.sessions.send(self.filter, commands, *args, **kwargs)[0]

    def copyfile(self, source, destination):

        # username, password = BACKDOOR_CREDENTIALS
        #
        # scp_cmd = "scp -q {} {}@{}:{}"
        #
        # child = pexpect.spawn(scp_cmd.format(source, username, self.host,
        #                                      destination))
        # _ssh_send_pass(child, password)
        #
        # child.close()
        backdoor.copy(self.host, source, destination)

    def repave(self, config, startup=False):
        """overwrites running configuration"""

        repave_config = "/tmp/shakedown_repave_config"

        fd, path = tempfile.mkstemp()

        try:
            with os.fdopen(fd, 'w') as tmp:
                # do stuff with temp file
                tmp.write(config)
                tmp.close()
                self.copyfile(path, repave_config)
        finally:
            os.remove(path)

        self.execute([
            "bash timeout 30 sudo chmod 644 %s" % repave_config,
            ])

        if startup == True:
            self.execute([
                "copy startup-config repave-backup",
                "copy file:%s startup-config" % repave_config,
            ])
        else:
            self.execute("configure replace file:%s")


        self.execute(["bash timeout 30 sudo rm -f %s" % repave_config])

    def reimage(self, image):
        response = self.configure(["boot system %s" % image])[0]

    def revert(self):
        """revert the running configuration the startup configuration"""
        self.execute(["configure replace startup-config"])

    def reload(self, save=False, wait=False):
        username, password = BACKDOOR_CREDENTIALS

        _spawn = functools.partial(pexpect.spawn, "ssh %s@%s" % (username, self.host))
        #child = _ssh_spawn(self.host, username, password)
        child = _spawn()

        _ssh_send_pass(child, password)

        if save:
            child.sendline(r'Cli -p 15 -c write')

        child.sendline(r'echo reload now | Cli -p 15')
        #child.sendline("uname -a")
        index = child.expect([r'(\$|#) ?', pexpect.EOF])

        if index == 0:
            child.terminate()

        if wait:
            time.sleep(10)
            while True:
                try:
                    with eapi.Session(self.host, auth=tuple(self.creds)) as sess:
                        sess.send(["show hostname"])
                        break
                except eapi.EapiError:
                    pass

                #printf("host is not up yet")

        time.sleep(30)

    def reload_and_wait(self):
        self.reload(wait=True)
