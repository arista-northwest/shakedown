# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import copy
import pytest
import re
import functools
from shakedown.util import to_list, merge
from shakedown.config import config as sdconfig_
from shakedown.session import sessions as sessions_
#from shakedown.scout import api as scout_
from shakedown import scout as scout_

@pytest.fixture(scope="module")
def sdconfig():
    return copy.copy(sdconfig_)

@pytest.fixture(scope="session")
def sessions():
    """gets available connnections"""
    return sessions_

@pytest.fixture(scope="session")
def scout():
    scout_.gather()
    return scout_

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

@pytest.fixture()
def dut(sessions):
    return Dut(sessions, r"dut")

@pytest.fixture()
def sdut(sessions):
    return Dut(sessions, r"sdut")

@pytest.fixture(scope="module")
def testconfig(request):

    names = [request.module.__name__]
    tests = sdconfig_.mount("tests")
    filtered = {}

    vars = sdconfig_.mount("vars")

    _match = re.search(r"test_(\d+_([\w_]+))", names[0])
    if _match:
        for item in _match.groups():
            names.append(item)

    for item in names:
        if item in tests:
            filtered = tests[item]

    return merge(filtered, vars)
