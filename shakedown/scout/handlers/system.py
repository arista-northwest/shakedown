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

CMDS = [
    ("info", ["show hostname", "show version"], h_sysinfo)
]
