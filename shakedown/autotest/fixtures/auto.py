# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pytest
import functools
import datetime
import os
import warnings
import yaml
import subprocess
import shlex
import time
import pexpect
from pexpect import pxssh

from shakedown.autotest.report import report_store
from shakedown.autotest import dut as dut_
from shakedown.autotest import util
from shakedown.util import mkdir, indentblock
from shakedown.autotest.constants import SSH_INIT_REGEX, BACKDOOR_CREDENTIALS

@pytest.fixture(scope="module", autouse=True)
def _auto_load_module(request, sdconfig):
    header = yaml.full_load(request.module.__doc__)

    # merge any settings into copy of configuration
    if "settings" in header:
        sdconfig.merge("settings:\n  {}".format(header["settings"]))

@pytest.fixture(scope="module", autouse=True)
def _auto_output_dir(request):
    output_dir = request.config.getoption("output_dir")
    if output_dir:
        output_dir = os.path.expanduser(output_dir)
        output_dir = os.path.join(output_dir, request.module.__name__)
        mkdir(output_dir)

@pytest.fixture(scope="function", autouse=True)
def _auto_monkeypatch_send(duts, dut, sdut, request):

    def _yamlify(response):
        doc = ['host: {}'.format(response.session.hostaddr)]
        
        doc.append('commands:')

        for item in response:
            doc.append('  - command: {}'.format(item.command))
            if item.text:
                doc.append('    output: |')
                doc.append(indentblock(str(item.text), spaces=6))

        return '\n'.join(doc)

    def _callback(response):

        nodeid = request.node.nodeid
        path, _, _ = util.split_nodeid(nodeid)

        if path in report_store:
            sdreport = report_store[path]
            section = sdreport.get_section(nodeid)
            text = _yamlify(response)
            section.append("codeblock", text)

    for obj in [dut, sdut, duts]:
        def _rollback():
            obj.callback = None
        request.addfinalizer(_rollback)
        obj.callback = _callback

@pytest.fixture(scope="module", autouse=True)
def _auto_rollback(sessions, request, sdconfig):

    if not sdconfig["settings"].get("auto_rollback"):
        return

    now = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    backup = 'flash:snapshot-config-{}'.format(now)

    def _rollback():
        responses = sessions.send("s?dut", "diff startup-config running-config")
        for resp in responses:
            diff_ = resp[0].output.strip()
            if diff_:
                sessions.send(resp.session.hostaddr, [
                    'configure replace {}'.format(backup)
                ])

        sessions.send("s?dut", ['delete {}'.format(backup)])

    request.addfinalizer(_rollback)

    sessions.send("s?dut", "copy running-config {}".format(backup))

@pytest.fixture(scope="session", autouse=True)
def _auto_backdoor(sessions, request):

    # def _rollback():
    #     sessions.send(".*", [
    #         "configure",
    #         "no aaa root",
    #         "end",
    #         "write"
    #     ])
    # request.addfinalizer(_rollback)

    sessions.send("s?dut", [
        "configure",
        "aaa root secret root",
        "end",
        "write"
    ])

@pytest.fixture(scope="session", autouse=True)
def _auto_install_arstat(sessions, request):
    filtered = sessions.filter(r"s?dut")

    username, password = BACKDOOR_CREDENTIALS

    dir = os.path.dirname(os.path.abspath(__file__))
    path = "%s/../../../scripts/arstat" % dir

    for sess in filtered:

        scp = pexpect.spawn("scp %s %s@%s:/persist/local/arstat" % (path, username, sess.endpoint))
        index = scp.expect(SSH_INIT_REGEX)
        if index == 0:
            scp.sendline("yes")
            index = scp.expect(SSH_INIT_REGEX)

        if index == 1:
            scp.sendline(password)
            scp.expect(pexpect.EOF)
        scp.close()
