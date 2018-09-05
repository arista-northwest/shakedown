# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from shakedown.scout import api

def get_bgp_asn(filter, vrf="default"):
    return [
        {k:item[k] for k in ['_dut', 'asn']}
        for item in api.find("bgp.summary", "dut", query={"vrf": vrf})
    ]

def get_management_intf(filter):

    return api.find_one("interfaces.status", filter, query={
        "name": {"$regex": "Management"},
        "protocol_status": "up",
        "primary_ip": {"$ne": "0.0.0.0"}
    })

def get_viable_bgp_peers(filter):
    return api.find("bgp.peers", filter, query={"state": "Established"})

def get_viable_bgp_session(afilter, bfilter=".*"):

    aside = None
    bside = None

    peers = get_viable_bgp_peers(afilter)

    for aside in peers:
        #print(peer)
        bside = api.find_one("bgp.peers", bfilter, query={
            "update_source": aside["address"],
            "state": "Established"
        })
        if bside:
            break

    return (aside, bside)

def get_viable_portchannel(filter, other):

    ports = [
        {key:item[key] for key in ["name", "local_port", "port"]}
        for item in api.find("lldp.neighbors", filter,
                             query={"name": {"$regex": other}})
    ]

    for port in ports:
        remote = None
        local = api.find_one("lag.members", filter, query={
            "port": port["local_port"],
            "active": True
        })

        if local:
            remote = api.find_one("lag.members", other, query={
                "port": port["port"],
                "active": True
            })

            if remote:
                return(local["name"], remote["name"])

    return (None, None)

def get_viable_lag_member_neighbor(filter, name):

    local = api.find_one("lag.members", filter, query={
        "name": name,
        "active": True
    })

    if local:
        neighbor = api.find_one("lldp.neighbors", filter, query={
            "local_port": local["port"]
        })

        if neighbor:
            dut = api.find_one("system.info", query={
                "fqdn": neighbor["name"]
            })["_dut"]

            return ((local["_dut"], local["port"]), (dut, neighbor["port"]))