# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pytest
import functools
import datetime
import os
import warnings
import yaml

from shakedown.autotest.report import report_store
from shakedown.autotest import util

from pprint import pprint

@pytest.fixture(scope="module", autouse=True)
def _auto_load_module(request, sdconfig):

    header = yaml.load(request.module.__doc__)

    # merge any settings into copy of configuration
    if "settings" in header:
        sdconfig.merge("settings:\n  {}".format(header["settings"]))


@pytest.fixture(scope="function", autouse=True)
def _auto_monkeypatch_send(sessions, request):
    """Monkey patch the send method to call us back when any commands are
    sent"""

    def _callback(response):

        nodeid = request.node.nodeid
        path, _, _ = util.split_nodeid(nodeid)

        if path in report_store:
            sdreport = report_store[path]
            section = sdreport.get_section(nodeid)
            target = response.parent.host
            text = "{}# {}\n{}".format(target, response.command, str(response))
            section.append("codeblock", text)

    def _restore_send():
        sessions.send = sessions._session_monitor_send
        del sessions._session_monitor_send

    request.addfinalizer(_restore_send)

    sessions._session_monitor_send = sessions.send
    sessions.send = functools.partial(sessions._session_monitor_send,
                                      callback=_callback, raise_for_error=True)

@pytest.fixture(scope="module", autouse=True)
def _auto_rollback(sessions, request, sdconfig):

    if not sdconfig["settings"].get("auto_rollback"):
        return

    now = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    backup = 'flash:snapshot-config-{}'.format(now)

    def _rollback():
        responses = sessions.send(".*", "diff startup-config running-config")

        for resp in responses:
            diff_ = resp[0].output.strip()
            if diff_:
                response = sessions.send(resp.host, [
                    'configure replace {}'.format(backup)
                ])

        response = sessions.send(".*", ['delete {}'.format(backup)])

    request.addfinalizer(_rollback)

    response = sessions.send(".*", "copy running-config {}".format(backup))

@pytest.fixture(scope="module", autouse=True)
def _auto_backdoor(sessions, sdconfig, request):

    def _rollback():
        sessions.send(".*", [
            "configure",
            "no aaa root",
            "end"
        ])
    request.addfinalizer(_rollback)

    sessions.send(".*", [
        "configure",
        "aaa root secret root",
        "end"
    ])
