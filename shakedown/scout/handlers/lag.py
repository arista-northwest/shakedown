# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

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

def h_details(responses):
    #
    # lags = responses[0]["portChannels"]
    lags = []
    for name, data in responses[0]["portChannels"]:
        for port, details in data["inactivePorts"]:

            lags.append({
                "port": port,
                "protocol": data["protocol"],
                "mode": data["lacpMode"],
                "active": False
            }

        for port, details in data["activePorts"]:

            lags.append({
                "port": port,
                "protocol": data["protocol"],
                "mode": data["lacpMode"],
                "active": True
            })
    return lags

CMDS = [
    ("members", ["show port-channel all-ports detailed"], h_details)
]
