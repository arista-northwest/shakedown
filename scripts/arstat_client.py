#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from __future__ import print_function

import sys
import time
import json
from pprint import pprint
from datetime import datetime

try:
    import pandas as pd
    import numpy
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as pyplot
except ImportError:
    raise ValueError(('SciPy stack is not install. Please install it '
                      'from http://www.scipy.org/install.html to use '
                      'this class'))
import signal

def floor_timestamps(timestamps):

    for timestamp in timestamps:
        timestamp = datetime.fromtimestamp(timestamp)

def update(dataframe, data, timestamps=None, freq=None):
    """\
    accepts data in 2 forms:
        {"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}
        [[1, 2 ,3 ,4], [1, 2 ,3 ,4]]

    timestamps args can be in the following combinations:
        timestamps # alone
        start + freq
        end + freq
    """

    index = pd.to_datetime(timestamps)

    newframe = pd.DataFrame(data, index, columns=list(data.keys()),
                             dtype=numpy.float)

    return dataframe.combine_first(newframe)

def topn(dataframe, top=10):
    counted_ = dataframe.count()
    counted_.sort_values(ascending=False)
    return dataframe[list(counted_[:top].keys())]

def tail(dataframe, rows=5):
    return dataframe.tail(rows)

def plot(dataframe, path=None, top=10, title=None, ylabel=None, width=12,
         height=6):
    dataframe = topn(dataframe, top).plot(figsize=(width, height))
    pyplot.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    if title:
        pyplot.title(title)
    if ylabel:
        pyplot.ylabel(ylabel)
    if path:
        pyplot.savefig(path, bbox_inches='tight')
    else:
        pyplot.show()

def parse_data(data, name, tag):
    parsed = {}
    for entry in data:
        if entry["name"] == name:
            value = entry["cpu_usage"]
            
            if not tag in entry["tags"]:
                raise ValueError("Tag '%s' does not exist" % tag)
            
            key = entry["tags"][tag]

            parsed[key] = value

    return parsed

def main():
    import argparse

    parser = argparse.ArgumentParser(prog="arcomm")
    parser.add_argument("-d", "--delimeter",
                        help="Specifies the field delimeter.")
    parser.add_argument("-j", "--json", action="store_true",
                        help="Output JSON instead of plain text")
    parser.add_argument("-p", "--periods", default=60, type=int,
                        help="Specify number of records to keep.")
    parser.add_argument("-n", "--name", default=None,
                        help="plot name. i.e. -t proc.stat.cpu")
    parser.add_argument("-t", "--tag",
                        help="use tag for data label")
    parser.add_argument("-v", "--version", action="store_true",
                        help="Display version info")
    parser.add_argument("--plot", action="store_true", default=True)
    parser.add_argument("--plot-title", default="[Untitled]",
                        help="Specify a plot title")
    parser.add_argument("--plot-ylabel", default="[untitled]",
                        help="Specifies a y-axis label")
    parser.add_argument("--plot-file", help="Specify file to save plot image")
    parser.add_argument("--plot-topn", default=10, help="Plot top N entries")

    args = parser.parse_args()

    dataframe = pd.DataFrame()
    sorted_df = None

    def sigint_handler(sig, frame):
        print(sorted_df)
        if args.plot_file:

            print("plotting...")
            plot(sorted_df, args.plot_file, top=args.plot_topn,
                 title=args.plot_title, ylabel=args.plot_ylabel)

        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            data = json.loads(line)
            try:
                dataframe = update(dataframe, parse_data(data, args.name, args.tag),
                                   timestamps=[datetime.utcnow()])
            except ValueError:
                continue

            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                # count and sort by number of occurences
                counted = dataframe.count()
                sorted_ = counted.sort_values(ascending=False)
                sorted_df = dataframe[list(sorted_[:args.plot_topn].keys())]
                print(sorted_df.tail(1))

    except KeyboardInterrupt:
        pass

    if args.plot_file:
        print("plotting...")
        plot(sorted_df, args.plot_file, top=args.plot_topn,
             title=args.plot_title, ylabel=args.plot_ylabel)

if __name__ == '__main__':
    main()
