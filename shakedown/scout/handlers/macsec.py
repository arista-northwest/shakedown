
"""
{
    "interfaces": {
        "Ethernet7/16/1": {
            "portId": 1115,
            "address": "44:4c:a8:b7:ce:6c",
            "controlledPort": true,
            "keyNum": 1,
            "keyMsgId": "77a38260140c812ebf166d42"
        },
        "Ethernet7/30/1": {
            "portId": 1171,
            "address": "44:4c:a8:b7:cd:e0",
            "controlledPort": true,
            "keyNum": 1,
            "keyMsgId": "ce01e667dd6962fb300ab156"
        },
"""


def h_macsec_intf(responses):
    records = []
    for name, detail in responses[0]["interfaces"].items():
        records.append({
            "name": name,
            "address": detail["address"],
            "isup": False if detail["keyMsgId"] == None else True
        })
    return records

CMDS = [
    ("info", ["show mac security interface"], h_macsec_intf)
]
