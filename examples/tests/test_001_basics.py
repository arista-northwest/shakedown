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
import eapi
import random
import string

from pprint import pprint


def test_version(sessions, sdconfig, testconfig, sdreportsection):
    """Autotest will scan the class for any methods that start with 'test'."""

    version = testconfig["software_version"]
    responses = sessions.send(r"dut", "show version")

    for response in responses:
        assert version in response[0].output, \
            "Software version should be {}".format(version)

    sdreportsection.text("random link...")
    sdreportsection.link("http://httpbin.org/",
                         text="httpbin",
                         title="link to httpbin")


@pytest.mark.xfail
def test_bad_version(sessions, sdconfig, testconfig):
    """Set version to an old image.  Will fail"""
    version = "0.1.0"
    response = sessions.send(r"dut", "show version")

    for r in response:
        assert version in str(r[0].output), \
            "Software version should be {}".format(version)


def test_bogus(sessions, sdconfig, testconfig):
    """Runs a bogus command and `eapi.EapiResponseError` should raised"""

    with pytest.raises(eapi.EapiResponseError):
        sessions.send(r"dut", "show bogus")


def test_config(sessions):
    """If configuration changes are made inside a test module. They will be \
    rolled back"""
    secret = ''.join([
        random.choice(string.ascii_letters + string.digits) for n in range(8)
    ])
    sessions.send(
        r"dut",
        ["configure", "username timmy secret {}".format(secret), "end"])


def test_dut(dut):
    """The `dut` can still be used directly, if the tag is assigned properly \
    to a connection

    connections:
      veos-1:
        ...
        tags: [ dut, ... ]
    """

    dut.execute(["show version", "show hostname"])
    dut.configure(["username tommy nopassword"])


def test_sdut(sdut):
    """The `sdut` can still be used directly if the tag exists"""
    sdut.execute(["show version"])
    sdut.configure(["username tumi nopassword"])


@pytest.mark.xfail
def test_failure():
    """Force a failure"""
    assert True == False, "True does not equal False!"


def test_until(dut):
    """test until arg"""
    dut.execute("show clock",
                until={
                    "condition": r"\:\d5",
                    "timeout": 30,
                    "sleep": 1
                })


def test_backdoor(backdoor, dut):
    backdoor.send("uname -a")

    response = backdoor.repave(config="hostname sdfsdfgasdfg")

    print(response)