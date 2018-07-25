# -*- coding: utf-8 -*-
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
"""
title: Test BGP

description: |
    Test basic BGP functionality

settings:
    auto_rollback: true
"""

def test_sessions(scout, sessions):
    """Find connected interfaces and bgp peers.  Then, \
    assert that the session is established
    """
    interfaces = scout.find("interfaces.status", "s?dut", query={
        "primary_ip": {"$ne": None},
        "link_status": "connected"
    })

    assert len(interfaces) > 0, "Didn't find any interfaces..."

    for interface in interfaces:
        primary_ip = interface["primary_ip"]
        peers = scout.find("bgp.peers", query={"update_source": primary_ip})

        for peer in peers:

            commands = ["show ip bgp neighbors {}".format(peer["peer"])]
            responses = sessions.send(peer["_dut"], commands, encoding="text")

            for response in responses:
                assert "BGP state is Established" in str(response), \
                       "Peer state should be established"
