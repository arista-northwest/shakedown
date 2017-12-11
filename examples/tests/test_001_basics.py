# -*- coding: utf-8 -*-
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
"""
title: Defaults Collection

description: |
    Make sure the DUT is on the correct software version

settings:
    auto_rollback: true
"""
import re
import pytest
import arcomm

__version__ = "0.1.0"

def test_version(sessions, sdconfig, testconfig):
    """Autotest will scan the class for any methods that start with 'test'."""
    #print("TESTCONFIG:", testconfig)
    version = testconfig["software_version"]

    response = sessions.send(r"dut", "show version")

    for r in response:

        assert version in str(r[0].output), \
            "Software version should be {}".format(version)

def test_bogus(sessions, sdconfig, testconfig):
    """Run a bogus command. should throw error"""
    with pytest.raises(arcomm.ExecuteFailed):
        response = sessions.send(r"dut", "show bogus")

# def test_config(sessions):
#     """test if rollback is triggered"""
#     sessions.send(r"dut", ["configure", "username timmy nopassword", "end"])
