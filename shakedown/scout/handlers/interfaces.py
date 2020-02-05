# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
"""
{
    "interfaceStatuses": {
        "Management1": {
            "vlanInformation": {
                "interfaceMode": "routed",
                "interfaceForwardingModel": "routed"
            },
            "bandwidth": 1000000000,
            "interfaceType": "10/100/1000",
            "description": "",
            "autoNegotiateActive": true,
            "duplex": "duplexFull",
            "autoNegotigateActive": true,
            "linkStatus": "connected",
            "lineProtocolStatus": "up"
        },
        "Ethernet2": {
            "vlanInformation": {
                "interfaceMode": "routed",
                "interfaceForwardingModel": "routed"
            },
            "bandwidth": 0,
            "interfaceType": "EbraTestPhyPort",
            "description": "Link to veos-2-eth1",
            "autoNegotiateActive": false,
            "duplex": "duplexFull",
            "autoNegotigateActive": false,
            "linkStatus": "connected",
            "lineProtocolStatus": "up"
        },
"""

import re

from ipaddress import ip_address, ip_network

def intf_short_name(name):

    match = re.search(r"(ma|lo|et|po|vlan)[a-z\-]*([\d\/\.]+)", name, re.I)
    if match:
        return "".join(match.groups())

def intf_kernel_name(name):
    name = intf_short_name(name)

    if name:
        return name.replace("/", "_").lower()

def h_status(responses):
    records = []

    ip_interfaces = responses[1]["interfaces"]

    for name, status in responses[0]["interfaceStatuses"].items():

        primary_ip = "unassigned"
        primary_masklen = -1
        primary_network = "unassigned"
        mtu = -1
        vrf = "default"

        mode = status["vlanInformation"].get("interfaceForwardingModel")

        if mode == "routed" and name in ip_interfaces:
            _priip = ip_interfaces[name]["interfaceAddress"]["primaryIp"]

            primary_ip = _priip["address"]
            primary_masklen = _priip["maskLen"]
            primary_network = str(ip_network("{}/{}".format(_priip["address"],
                                                            _priip["maskLen"]),
                                                            False))
            mtu = ip_interfaces[name]["mtu"]
            vrf = ip_interfaces[name]["vrf"]

        records.append({
            "name": name,
            "short": intf_short_name(name),
            "kernel": intf_kernel_name(name),
            "mode": mode,
            "vlan": int(status["vlanInformation"].get("vlanId", -1)),
            "bandwidth": status["bandwidth"],
            "description": status["description"],
            "link_status": status["linkStatus"],
            "protocol_status": status["lineProtocolStatus"],
            "primary_ip": primary_ip,
            "primary_masklen": primary_masklen ,
            "primary_network": primary_network,
            "mtu": int(mtu),
            "vrf": vrf
        })

    return records

CMDS = [
    ("status", ["show interfaces status", "show ip interface"], h_status)
]
