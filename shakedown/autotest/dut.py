# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pexpect
import tempfile
import os
import functools
import time

from shakedown.util import to_list

class Dut():
    def __init__(self, sessions, filt):
        self.sessions = sessions
        self.filter = filt

        self.session = self.sessions.filter(filt)[0]

    @property
    def host(self):
        return self.session.endpoint

    hostname = host

    @property
    def creds(self):
        return self.session.creds

    @property
    def auth(self):
        return self.session.auth

    @property
    def protocol(self):
        return self.session.protocol

    def execute(self, commands, *args, **kwargs):
        commands = to_list(commands)
        return self.sessions.send(self.filter, commands, *args, **kwargs)[0]

    send = execute_until = execute

    def configure(self, commands, *args, **kwargs):
        commands = to_list(commands)
        commands = ["configure"] + commands + ["end"]
        return self.sessions.send(self.filter, commands, *args, **kwargs)[0]
