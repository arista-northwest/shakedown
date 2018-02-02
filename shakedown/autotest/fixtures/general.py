# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import copy
import pytest
import re

from shakedown.config import config as sdconfig_
from shakedown.session import sessions as sessions_

@pytest.fixture(scope="module")
def sdconfig():
    return copy.deepcopy(sdconfig_)

@pytest.fixture(scope="session")
def sessions():
    return sessions_

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
