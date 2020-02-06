# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pytest
from shakedown.backdoor import Session

@pytest.fixture(scope="module")
def backdoor(sessions, sdconfig, request):
    bkd = Session()
    request.addfinalizer(lambda: bkd.close())

    bkd.open(sessions.filter_one(r"dut").host)

    return bkd
