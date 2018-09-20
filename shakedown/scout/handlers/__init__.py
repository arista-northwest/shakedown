# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
from . import bgp, interfaces, system, lldp, lag, routes
handlers = [
    ("system", system),
    ("interfaces", interfaces),
    ("bgp", bgp),
    ("lldp", lldp),
    ("lag", lag),
    ("routes", routes)
]
