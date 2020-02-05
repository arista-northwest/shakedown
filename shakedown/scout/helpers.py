# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from shakedown.scout import api
from shakedown.scout import exceptions

def get_bgp_asn(filt, vrf="default"):
    return [
        {k:item[k] for k in ['_dut', 'asn']}
        for item in api.find("bgp.summary", filt, query={"vrf": vrf})
    ]

def get_management_intf(filt):

    return api.find_one("interfaces.status", filt, query={
        "name": {"$regex": "Management"},
        "protocol_status": "up",
        "primary_ip": {"$ne": "0.0.0.0"}
    })

def get_management_vrfs(filt):

     return [
        {k:item[k] for k in ['_dut', 'vrf']}
        for item in api.find("interfaces.status", filt, query={
                "name": {"$regex": "Management"},
                "protocol_status": "up",
                "primary_ip": {"$ne": "0.0.0.0"}
            })
    ]

def get_viable_bgp_peers(filt):
    return api.find("bgp.peers", filt, query={"state": "Established"})

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

def get_viable_bgp_ecmp_route(filt):
    return api.find_one("bgp.received_routes", filt, query={
        "isActive": True,
        "isEcmp": True,
        "isEcmpHead": True,
        "isEcmpContributor": True,
        "isValid": True
    })

def get_viable_portchannel_intf(filt, other):

    # ports = [
    #     {key:item[key] for key in ["name", "local_port", "port"]}
    #     for item in api.find("lldp.neighbors", filt,
    #                          query={"name": {"$regex": other}})
    # ]

    # for port in ports:
    #     remote = None
    #     local = api.find_one("lag.members", filt, query={
    #         "port": port["local_port"],
    #         "active": True
    #     })

    #     if local:
    #         remote = api.find_one("lag.members", other, query={
    #             "port": port["port"],
    #             "active": True
    #         })

    #         if remote:
    #             return(local["name"], remote["name"])
    
    a, b = get_viable_portchannel(filt, other)
    if a and b:
        return a["name"], b["name"]
    
    return (None, None)

def get_viable_portchannel(filt, other):

    ports = [
        {key:item[key] for key in ["name", "local_port", "port"]}
        for item in api.find("lldp.neighbors", filt,
                             query={"name": {"$regex": other}})
    ]

    for port in ports:
        remote = None
        local = api.find_one("lag.members", filt, query={
            "port": port["local_port"],
            "active": True
        })

        if local:
            remote = api.find_one("lag.members", other, query={
                "port": port["port"],
                "active": True
            })

            if remote:
                return(local, remote)

    return (None, None)

def get_viable_lag_member_neighbor(filt, name):

    local = api.find_one("lag.members", filt, query={
        "name": name,
        "active": True
    })

    if local:
        neighbor = api.find_one("lldp.neighbors", filt, query={
            "local_port": local["port"]
        })

        if neighbor:
            dut = api.find_one("system.info", ".*", query={
                "fqdn": neighbor["name"]
            })
            if not dut:
                raise exceptions.DutNotFoundException(
                    "Dut '{}' not found in scout database".format(neighbor["name"]))

            return ((local["_dut"], local["port"]), (dut["_dut"], neighbor["port"]))

def get_viable_ip_neighbor(dut, sdut):
    neighbors = api.find("ip.neighbors", "dut", query={})
    for neighbor in neighbors:
        b_interface = api.find_one("interfaces.status", r"sdut", query={
            "protocol_status": "up",
            "name": {"$regex": "Port|Eth"},
            "primary_ip": neighbor["address"]
        })

        if b_interface:
            a_interface = api.find_one("interfaces.status", r"dut", query={
                "name": neighbor["interface"]
            })
            return(a_interface, b_interface)

    return (None, None)

# def get_active_macsec_interfaces(filt):
#     return [
#         item["name"] for item in api.find("macsec.info", filt, query={"isup": True})
#     ]
