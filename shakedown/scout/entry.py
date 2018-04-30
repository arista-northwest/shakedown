# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

# import sys
# import os
# import tempfile
# import time
# from pprint import pprint
# from tinydb import TinyDB, Query, where
# from collections import OrderedDict
# from shakedown.config import config
# from shakedown.session import sessions
# from shakedown.scout import handlers
# from shakedown.util import unzip
# from tinydb.storages import MemoryStorage
#
# from shakedown.scout.database import Database

# # db = tinydb.TinyDB(os.path.join(tempfile.gettempdir(), "scoutdb.json"))
# db = Database(storage=MemoryStorage)
#
# def gather():
#     for _, handler in handlers.handlers:
#         for table, commands, callback in handler.CMDS:
#
#             #table = db["_".join([prefix, suffix])]
#             table = db[table]
#             responses = sessions.send("veos.*", list(commands), encoding='json')
#
#             for response in responses:
#                 hostaddr = response.host
#
#                 if response.status != "ok":
#                     continue
#
#                 response = callback(response.responses)
#
#                 if not isinstance(response, list):
#                     response = [response]
#
#                 for item in response:
#                     record = {"hostaddr": hostaddr, "timestamp": int(time.time()), **dict(item)}
#
#                     table.insert_one(record) #, Query()._id == _id)
#             #pprint(table.all())

# def main():
#     import argparse
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument("-c", "--config")
#     args = parser.parse_args()
#     config.load(args.config)
#
#     gather()
#
#     pprint(list(db.bgp_summary.find({"hostaddr": { "$regex": r"veos-[0-9]" } })))
#
# if __name__ == '__main__':
#     main()
