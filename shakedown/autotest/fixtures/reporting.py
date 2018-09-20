# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import pytest
import yaml

from shakedown.autotest.report import Report, report_store
from shakedown.util import mkdir
from shakedown.autotest import util

from shakedown.autotest import publishers

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

        output_dir = request.config.getoption("output_dir")
        pub_names = request.config.getoption("publish")

        if output_dir:
            output_dir = os.path.expanduser(output_dir)
            output_dir = os.path.join(output_dir, request.module.__name__)
            # mkdir(output_dir)

            data = report.to_dict()

            for name in pub_names:

                publisher = getattr(publishers, name)
                publisher.save(data, output_dir)

        del report_store[path]

    request.addfinalizer(_finish)

    return report

@pytest.fixture(scope="function")
def sdreportsection(request):

    nodeid = request.node.nodeid
    path, _, _ = util.split_nodeid(nodeid)

    sdreport = report_store[path]

    return sdreport.get_section(nodeid)

reportitem = sdreportsection
