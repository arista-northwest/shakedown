


def h_static_routes(responses):
    records = []
    for vrf, details in responses[0]["vrfs"].items():
        for destination, detail in details["routes"].items():
            for via in detail["vias"]:
                records.append({
                    "vrf": vrf,
                    "destination": destination,
                    "nexthop": via["nexthopAddr"],
                    "interface": via["interface"]
                })

    return records


CMDS = [
    ("static", ["show ip route vrf all static"], h_static_routes)
]
