# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

def h_neighbors(responses):

    results = []
    neighbors = responses[0]["lldpNeighbors"]
    detail = responses[1]["lldpNeighbors"]
    #pprint(neighbors)
    for neighbor in neighbors:
        local_port = neighbor["port"]
        n_detail = [
            neigh for neigh in detail[local_port]["lldpNeighborInfo"]
            if neigh["systemName"] == neighbor["neighborDevice"]
        ][0]

        results.append({
            "name": neighbor["neighborDevice"],
            "port": neighbor["neighborPort"],
            "chassis_id": n_detail["chassisId"],
            "description": n_detail["systemDescription"],
            "local_port": local_port
        })

    return results

CMDS = [
    ("neighbors", ["show lldp neighbors", "show lldp neighbors detail"], h_neighbors)
]
