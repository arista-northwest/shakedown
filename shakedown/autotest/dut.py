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

class Dut():
    def __init__(self, sessions, filt):
        self.sessions = sessions
        self.filter = filt

        self.filtered = self.sessions.filter(filt)

    @property
    def host(self):
        return self.filtered[0].endpoint

    hostname = host

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
        if wait and type(wait) is not int:
            wait = 3600

        with backdoor.Backdoor() as bkd:
            bkd.open(self.host)
            bkd.reload(save=save, waitfor=wait)

    def reload_and_wait(self, save=False):
        self.reload(save=save,wait=True)
