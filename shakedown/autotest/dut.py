# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pexpect
import tempfile
import os
import functools
import time

from shakedown.util import to_list
from shakedown import ssh
from shakedown.session import sessions

def record(func):
    def wrapper(*args, **kwargs):
        callback = args[0].callback
        resp = func(*args, **kwargs)
        if callback:
            callback(resp)
        return resp
    return wrapper

def _configure(commands):
    return ["configure"] + to_list(commands) + ["end"]

class Dut():
    def __init__(self, session, callback):
        self.session = session
        self.callback = callback

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

    @record
    def send(self, commands, *args, **kwargs):
        commands = to_list(commands)
        return self.session.send(commands, *args, **kwargs)[0]

    execute = execute_until = send

    def configure(self, commands, *args, **kwargs):
        return self.send(_configure(commands), *args, **kwargs)

    def ssh(self, auth=None):
        if not auth:
            auth = self.auth
        return ssh.session(self.host, auth=auth)

class DutManager():
    def __init__(self, callback=None):
        self.callback = callback

    def select(self, dut):
        return Dut(sessions.filter_one(dut), self.callback)

    #@record
    def send(self, patterns, commands, **kwargs):
        sessions.send(patterns, commands, **kwargs)
    
    execute = execute_until = send
    
    def configure(self, patterns, commands, **kwargs):
        return self.send(patterns, _configure(commands), **kwargs)