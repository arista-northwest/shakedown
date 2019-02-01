#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import time
import json
import os
from datetime import datetime
import time
import pytest

class ArstatClient():

    def __init__(self):
        self.datatype = numpy.float
        self.dataframe = pandas.DataFrame()
        self.sorted_df = pandas.DataFrame()


    def floor_timestamps(self, timestamps):

        for timestamp in timestamps:
            timestamp = datetime.fromtimestamp(timestamp)

    def update(self, data, timestamps=None, start=None, end=None,
               freq=None):
        """\
        accepts data in 2 forms:
            {"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}
            [[1, 2 ,3 ,4], [1, 2 ,3 ,4]]

        timestamps args can be in the following combinations:
            timestamps # alone
            start + freq
            end + freq
        """

        index = pandas.DatetimeIndex(timestamps, freq=freq, periods=1,
                                     start=start, end=end)

        newframe = pandas.DataFrame(data, index, columns=list(data.keys()),
                                 dtype=self.datatype)

        return self.dataframe.combine_first(newframe)

    def topn(self, top=10):

        with pandas.option_context('display.max_rows', None,
                                   'display.max_columns', None):
            # count and sort by number of occurences
            counted = self.dataframe.count()
            sorted_ = counted.sort_values(ascending=False)
            return self.dataframe[list(sorted_[:top].keys())]

    def tail(self, dataframe, rows=5):
        return self.dataframe.tail(rows)

    def plot(self, path=None, top=10, title=None, ylabel=None,
             width=12, height=6):

        topnframe = self.topn(top).plot(figsize=(width, height))
        pyplot.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
        if title:
            pyplot.title(title)
        if ylabel:
            pyplot.ylabel(ylabel)
        if path:
            pyplot.savefig(path, bbox_inches='tight')
        else:
            pyplot.show()

    def parse_data(self, data):
        parsed = {}
        for entry in data:
            if entry["name"] == "proc.stat.cpu.task":
                value = entry["cpu_usage"]
                name = entry["tags"]["task"]
                parsed[name] = value
        return parsed

    def feedline(self, line):
        data = json.loads(line.strip())
        ts = pandas.Timestamp(datetime.utcnow(), tz='utc')
        self.dataframe = self.update(self.parse_data(data),
                                     timestamps=[ts])
@pytest.fixture(scope="session")
def load_scipy():
    from pexpect import pxssh

    try:
        import pandas
        import numpy
        import matplotlib

        matplotlib.use('Agg')
        import matplotlib.pyplot as pyplot
    except ImportError:
        raise ValueError(('SciPy stack is not installed. Please install it '
                          'from http://www.scipy.org/install.html to use '
                          'this fixture'))

@pytest.fixture(scope="function")
def procplot(load_scipy, sessions, request, reportitem, filter="dut"):


    filtered = sessions.filter(filter)

    output_dir = request.config.getoption("output_dir")
    if not output_dir:
        return

    output_dir = os.path.join(output_dir, request.module.__name__)

    ssh_sessions = []

    def links():
        for (sess, client) in ssh_sessions:
            yield "{}-test.png".format(sess.endpoint)

    def _finish():
        for (sess, client) in ssh_sessions:
            client.send(chr(3))
            client.prompt()
            client.close()

            arstat = ArstatClient()
            for line in client.before.splitlines()[1:-1]:
                arstat.feedline(line.decode("utf-8"))

            path = "{}/{}-test.png".format(output_dir, sess.endpoint)
            arstat.plot(path, top=10,
                        title="CPU Utilization for {}".format(sess.endpoint),
                        ylabel=r'% cpu')
            reportitem.image("{}-test.png".format(sess.endpoint))
    request.addfinalizer(_finish)

    for sess in filtered:

        client = pxssh.pxssh()
        client.login(sess.endpoint, username="root", password="root")
        client.sendline("python /persist/local/arstat -i 1 -j")
        ssh_sessions.append((sess, client))
