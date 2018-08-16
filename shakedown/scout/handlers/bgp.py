# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
from pprint import pprint
def h_summary(responses):
    records = []
    for vrf, summary in responses[0]["vrfs"].items():
        records.append({
            "vrf": vrf,
            "asn": summary["asn"],
            "router_id": summary["routerId"]
        })
    return records

def h_peers(responses):
    records = []
    for vrf, peers in responses[0]["vrfs"].items():
        for peer in peers["peerList"]:

            records.append({
                "vrf": vrf,
                "type": peer["linkType"],
                "address": peer["peerAddress"],
                "local_asn": int(peer["localAsn"]),
                "local_router_id": peer["localRouterId"],
                "asn": int(peer["asn"]),
                "router_id": peer["routerId"],
                "interface": peer.get("ifName", ""),
                "group": peer.get("peerGroup", ""),
                "update_source": peer.get("updateSource"),
                "state": peer["state"]
            })
    return records

CMDS = [
    ("summary", ["show ip bgp summary"], h_summary),
    ("peers", ["show ip bgp neighbors"], h_peers)
]
