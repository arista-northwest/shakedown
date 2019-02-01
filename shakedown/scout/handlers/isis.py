# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

def h_summary(responses):
    records = []
    for vrf, instances in responses[0]["vrfs"].items():
        for instance, neighbors in instances["isisInstances"].items():
            for neighbor, adjacencies in neighbors["neighbors"].items():
                for adj in adjacencies["adjacencies"]:
                    records.append({
                        "vrf": vrf,
                        "instnace": instance,
                        "neighbor": neighbor,
                        "state": adj["state"],
                        "level": adj["level"],
                        "snpa": adj["snpa"],
                        "circuit_id": adj["circuitId"],
                        "interface": adj["interfaceName"],
                        "hostname": adj["hostname"],
                        "ipv4_address": adj['details']["ip4Address"],
                    })
    return records

CMDS = [
    ("summary", ["show isis neighbors"], h_summary)
]
