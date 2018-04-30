# -*- coding: utf-8 -*-
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
"""
title: Test Syslog

description: |
    Test basic Syslog functionality

settings:
    auto_rollback: true
"""

from pprint import pprint
import time

def test_intf_up_down(sessions, scout, request):
    """Test syslog messages for interface up/down events"""

    neighbor = scout.find_one("lldp.neighbors", "dut", query={
        "port": {"$regex": "Ethernet"}
    })

    local_port = neighbor["local_port"]

    t1 = int(time.time()) - 5

    sessions.send("dut", "show interfaces {} status".format(neighbor["local_port"]))

    sessions.send(neighbor["name"], [
        "configure",
        "interface {}".format(neighbor["port"]),
        "shutdown",
        "exit",
        "end"
    ])

    time.sleep(5)
    sessions.send("dut", "show interfaces {} status".format(neighbor["local_port"]),
        until="notconnect")

    sessions.send(neighbor["name"], [
        "configure",
        "interface {}".format(neighbor["port"]),
        "no shutdown",
        "exit",
        "end"
    ])

    sessions.send("dut", "show interfaces {} status".format(neighbor["local_port"]),
                      until=r"connected")

    t2 = int(time.time())

    responses = sessions.send("dut",
        "show logging last {} seconds | include changed state to up".format(t2 - t1))

    assert r"%LINEPROTO" in str(responses[0]), r"Should have seen LINEPROTO messages"
