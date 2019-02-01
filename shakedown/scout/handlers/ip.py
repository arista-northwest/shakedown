# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

def h_arp(responses):
    results = []
    neighbors = responses[0]["ipV4Neighbors"]

    for neighbor in neighbors:
        results.append({
            "mac_address": neighbor["hwAddress"],
            "address": neighbor["address"],
            "interface": neighbor["interface"],
            "static": False if neighbor["age"] else True
        })
    return results

CMDS = [
    ("neighbors", ["show ip arp"], h_arp)
]
