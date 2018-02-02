# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import pytest
import json

from shakedown.config import config as sdconfig
from shakedown.session import sessions
from shakedown.autotest import util

from shakedown.autotest.report import report_store

reportlog = []

def pytest_addoption(parser):
    """pytest hook for adding conosole options"""

    group = parser.getgroup("autotest", "autotest network device testing")

    group.addoption("--config", action="store", dest="sdconfig",
                    metavar="CONFIG")

    # does not work... why?
    # group.addoption("--working-dir", action="store", metavar="WORKING_DIR",
    #                 help=("base directory for tests, templates and "
    #                       "configuration.  By default use current dir"))

    group.addoption("--output-dir", action="store", metavar="OUTPUT_DIR",
                    help="base directory for reports")

    group.addoption("--publish", action="append", default=[],
                    metavar="PUBLISH",
                    help="Publish report to specified service")

    group.addoption("--option", help="user defined extra options")

@pytest.mark.tryfirst
def pytest_configure(config):

    if config.getoption("help"):
        return

    if not config.getoption("sdconfig"):
        pytest.exit("config option is required")

    # does not work... why?
    # working_dir = config.getoption("working_dir") or os.getcwd
    # os.chdir(working_dir)

    with open(config.getoption("sdconfig"), "r") as fh:
        sdconfig.merge(fh.read())

def pytest_unconfigure(config):
    """pytest hook - called after all tests have completed"""

    output_dir = config.getoption("output_dir")
    path = os.path.join(output_dir, "reportlog.json")
    with open(path, "w") as fh:
        fh.write(json.dumps(reportlog, indent=2, separators=(',', ': ')))

def pytest_runtest_setup(item):
    """run before executing test"""

def pytest_runtest_teardown(item):
    """Call after the test completes to update the report description"""

    nodeid = item.nodeid
    path, _, _ = util.split_nodeid(item.nodeid)

    if path in report_store:
        sdreport = report_store[path]
        section = sdreport.get_section(nodeid)
        section.description = item.function.__doc__

        # keep a log of outcomes for index page
        reportlog.append({
            "path": path,
            "nodeid": nodeid,
            "description": section.description,
            "outcome": section.outcome
        })

def pytest_runtest_logreport(report):
    """Call after the test completes to update the outcome and trace"""

    nodeid = report.nodeid
    path, _, _ = util.split_nodeid(nodeid)

    if report.when == "call":
        if path in report_store:
            sdreport = report_store[path]
            section = sdreport.get_section(nodeid)
            section.outcome = report.outcome
            section.traceback = report.longrepr
