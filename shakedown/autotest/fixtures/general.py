# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import copy
import pytest
import re
import functools
import os
import pexpect
from shakedown.util import to_list, merge
from shakedown.config import config as sdconfig_
from shakedown.session import sessions as sessions_
from shakedown.autotest.dut import Dut
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
    #scout_.gather("s?dut")
    return scout_

@pytest.fixture(scope="module")
def dut(sessions):
    return Dut(sessions, r"dut")

@pytest.fixture(scope="module")
def sdut(sessions):
    if sessions.filter(r"sdut"):
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
