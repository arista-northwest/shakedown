# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

def h_neighbors(responses):
    results = []
    neighbors = responses[0]["ipV6Neighbors"]

    for neighbor in neighbors:
        results.append({
            "mac_address": neighbor["hwAddress"],
            "state": neighbor["state"],
            "address": neighbor["address"],
            "interface": neighbor["interface"]
        })
    return results

CMDS = [
    ("neighbors", ["show ipv6 neighbors"], h_neighbors)
]
