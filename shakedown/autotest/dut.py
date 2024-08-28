# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from typing import Optional

from shakedown.util import to_list
from shakedown import ssh
from shakedown.session import sessions

def record(func):
    def wrapper(*args, **kwargs):
        callback = args[0].callback
        responses = func(*args, **kwargs)
        if callback:
            for resp in to_list(responses):
                callback(resp)
        return responses
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

    def get(self, pattern: str) -> Optional[Dut]:
        sess = sessions.filter_one(pattern)
        
        if sess:
            return Dut(sess, self.callback)
        
        return None
    
    select = get

    def send(self, patterns, commands, *args, **kwargs):
        return self.get(patterns).send(commands, *args, **kwargs)
    
    execute = execute_until = send
    
    def configure(self, patterns, commands, **kwargs):
        return self.send(patterns, _configure(commands), **kwargs)