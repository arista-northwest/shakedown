# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import copy
import pytest
import re
import functools
import os
import warnings

from shakedown.util import merge, indentblock
from shakedown.autotest.util import split_nodeid
from shakedown.autotest.report import report_store
from shakedown.config import config as sdconfig_
from shakedown.session import sessions as sessions_
from shakedown.autotest.dut import Dut, DutManager
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
    return scout_

@pytest.fixture(scope="function")
def duts(request):
    return DutManager()

connections = duts

@pytest.fixture(scope="function")
def dut(duts):
    dut = duts.select(r"dut")
    if not dut:
        raise ValueError("Tag 'dut' is not defined")
    
    print(f"DUT: {dut.session.endpoint} CB: {dut.callback}")
    dut.callback = duts.callback
    return dut

@pytest.fixture(scope="function")
def sdut(duts):
    sdut = duts.select(r"sdut")
    
    if not sdut:
        raise ValueError("Tag 'sdut' is not defined")
    
    sdut.callback = duts.callback
    return sdut

@pytest.fixture(scope="module")
def testconfig(request):

    names = [request.module.__name__]
    tests = sdconfig_.mount("tests")
    filtered = {}

    vars_ = sdconfig_.mount("vars")

    _match = re.search(r"test_(\d+_([\w_]+))", names[0])
    if _match:
        for item in _match.groups():
            names.append(item)

    for item in names:
        if item in tests:
            filtered = tests[item]

    return merge(filtered, vars_)
