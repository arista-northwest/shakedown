# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import copy
import pytest
import re
import functools
from shakedown.util import to_list
from shakedown.config import config as sdconfig_
from shakedown.session import sessions as sessions_

@pytest.fixture(scope="module")
def sdconfig():
    return copy.deepcopy(sdconfig_)

@pytest.fixture(scope="session")
def sessions():
    return sessions_

class Dut():
    def __init__(self, sessions, filt):
        self.sessions = sessions
        self.filter = filt
    def execute(self, commands, *args, **kwargs):
        commands = to_list(commands)
        return self.sessions.send(self.filter, commands, *args, **kwargs)[0]

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
    mounted = sdconfig_.mount("tests")

    _match = re.search(r"test_(\d+_([\w_]+))", names[0])
    if _match:
        for item in _match.groups():
            names.append(item)

    for item in names:
        if item in mounted:
            return mounted[item]

    return {}
