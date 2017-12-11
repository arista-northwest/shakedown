# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import pytest
import yaml

from shakedown.autotest.report import Report, report_store
from shakedown.autotest import util
__all__ = ["sdreport"]

@pytest.fixture(scope="module", autouse=True)
def sdreport(request):

    nodeid = request.node.nodeid
    path, _, _ = util.split_nodeid(nodeid)

    name = request.module.__name__
    header = yaml.load(request.module.__doc__)

    title = header.get("title", name)
    description = header.get("description", "")
    report = Report(title.strip(), description.strip())

    report_store[path] = report

    def _finish():

        output_dir = request.config.getoption('output_dir')

        if output_dir:
            output_dir = os.path.expanduser(output_dir)
            ofile = os.path.join(output_dir, request.module.__name__,
                                     "report.json")
            report.save(ofile)

        del report_store[path]

    request.addfinalizer(_finish)

    return report
