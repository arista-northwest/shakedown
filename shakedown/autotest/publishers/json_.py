# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import json

def render(data):
    return json.dumps(data, indent=2, separators=(',', ': '))

def save(data, path):
    path = os.path.join(path, "report.json")
    with open(path, "w") as fh:
        fh.write(render(data))
