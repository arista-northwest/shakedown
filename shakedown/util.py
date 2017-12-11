# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import sys

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

def plush(data):
    """print and flush"""
    sys.stdout.write(data)
    sys.stdout.flush()
    #sys.stderr.flush()
