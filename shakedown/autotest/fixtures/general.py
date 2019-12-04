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
    def _yamlify(response):
        doc = ['host: {}'.format(response.session.hostaddr)]
        #doc.append('code: {}'.format(response.code))
        doc.append('commands:')

        for item in response:
            doc.append('  - command: {}'.format(item.command))
            if item.text:
                doc.append('    output: |')
                doc.append(indentblock(str(item.text), spaces=6))

        return '\n'.join(doc)
    
    def _callback(response):
        nodeid = request.node.nodeid
        path, _, _ = split_nodeid(nodeid)

        if path in report_store:
            sdreport = report_store[path]
            section = sdreport.get_section(nodeid)
            text = _yamlify(response)
            section.append("codeblock", text)
    return DutManager(callback=_callback)

connections = duts

@pytest.fixture(scope="function")
def dut(duts):
    return duts.select(r"dut")

@pytest.fixture(scope="function")
def sdut(duts):
    return duts.select(r"sdut")

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
