# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import re

"""
{
    "portChannels": {
        "Port-Channel2": {
            "recircFeature": [],
            "fallbackState": "unconfigured",
            "inactivePorts": {},
            "activePorts": {
                "Ethernet2": {
                    "protocol": "lacp",
                    "lacpMode": "active",
                    "timeBecameActive": 1524426847.1184797
                }
            }
        }
    }
}
"""

def h_members(responses):
    members = []
    for name, data in responses[0]["portChannels"].items():
        id_ = int(re.match(r"port-channel\s*(\d+)", name, re.I).group(1))
        for port, details in data["inactivePorts"].items():
            members.append({
                "name": name,
                "id": id_,
                "port": port,
                "protocol": details.get("protocol") or "",
                "mode": details.get("lacpMode") or "",
                "active": False
            })

        for port, details in data["activePorts"].items():
            members.append({
                "name": name,
                "id": id_,
                "port": port,
                "protocol": details.get("protocol") or "",
                "mode": details.get("lacpMode") or "",
                "active": True
            })
    return members

CMDS = [
    ("members", ["show port-channel all-ports detailed"], h_members)
]
