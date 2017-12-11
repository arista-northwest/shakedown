# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import re

def split_nodeid(nodeid):
    """Split the nodied into a 3-tuple of path, function and param"""
    match = re.match(r"([\/\w_\-\.]+)(?:\:\:(\w+)(?:\[(.*)\])?)?", nodeid)
    if match:
        return tuple(match.groups())
