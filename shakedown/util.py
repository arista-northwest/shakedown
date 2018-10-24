# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import sys
import pprint
import difflib
import re

def column(data, offset=0, delimeter=r"\s+"):
    """Return the specified column from data"""
    results = []
    for line in data.splitlines():
        split_line = re.split(delimeter, line)
        results.append(split_line[offset])
    return "\n".join(results)

def grep(regex, data, flags=0):
    """Clone of *nix grep"""
    results = []
    for line in data.splitlines():
        if re.search(regex, line, flags):
            results.append(line)
    return "\n".join(results)
def to_list(data):
    """Creates a list containing the data as a single element or a new list
    from the original if it is already a list or a tuple"""
    if isinstance(data, (list, tuple)):
        return list(data)
    elif data is not None:
        return [data]
    else:
        return []

def merge(destination, source):
    for (key, value) in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(node, value)
        elif isinstance(value, (tuple, list)):
            if key not in destination:
                destination[key] = []
            destination[key] += value
        else:
            destination[key] = value

    return destination

def mkdir(path):
    """Create a directory and ignore directory already exists errors"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        import errno
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def plush(data=""):
    """print and flush"""
    sys.stdout.write(data)
    sys.stdout.flush()

def pplush(data="", **kwargs):
    plush(pprint.pformat(data, **kwargs))

def unzip(zipped):
    return list(zip(*zipped))

def udiff(left, right):
    """Show the differences between two multiline strings"""
    _diff = []
    for line in difflib.unified_diff(left.splitlines(), right.splitlines()):
        _diff.append(line)
    return "\n".join(_diff)

def uniq(lst):
    return list(set(lst))
