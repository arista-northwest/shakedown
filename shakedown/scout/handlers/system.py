# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from pprint import pprint

def h_sysinfo(response):
    return [{
        "sysname": response[0]["hostname"],
        "fqdn": response[0]["fqdn"],
        "version": response[1]["version"],
        "model": response[1]["modelName"],
        "serial": response[1]["serialNumber"],
        "sysmac":  response[1]["systemMacAddress"]
    }]

"""
{
    "peers": {
        "shakedown.lab.lan": {
            "delay": 0.524,
            "jitter": 0.294,
            "lastReceived": 1550009437.0,
            "peerType": "unicast",
            "reachabilityHistory": [
                true
            ],
            "condition": "sys.peer",
            "offset": 0.118,
            "peerIpAddr": "192.168.56.10",
            "pollInterval": 64,
            "refid": "98.152.165.38",
            "stratumLevel": 2
        }
    }
}
"""
def h_ntp(response):
    for name, peer in response[0]["peers"].items():
        return[{
            "name": name,
            "type": peer["peerType"],
            "address": peer["peerIpAddr"],
            "stratum": peer["stratumLevel"]
        }]
CMDS = [
    ("info", ["show hostname", "show version"], h_sysinfo),
    ("ntp", ["show ntp associations"], h_ntp)
]
