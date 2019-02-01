# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
from . import bgp, interfaces, ip, ipv6, isis, lag, lldp, macsec, routes, \
              system
handlers = [
    ("system", system),
    ("interfaces", interfaces),
    ("ip", ip),
    ("ipv6", ipv6),
    ("bgp", bgp),
    ("lldp", lldp),
    ("lag", lag),
    ("routes", routes),
    ("macsec", macsec),
    ("isis", isis)
]
