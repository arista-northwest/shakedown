# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
import sys
import os
import time
import logging
from shakedown.scout.database import Database
from shakedown.config import config
from shakedown.session import sessions
from shakedown.scout import handlers
from shakedown.util import to_list
from pprint import pprint

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

database = Database()

def gather(tables=[], endpoints=r".*"):
    tables = to_list(tables)

    for h_name, handler in handlers.handlers:
        for key, commands, callback in handler.CMDS:

            t_name = h_name + "." + key
            #print("gathering...", type(t_name, tables, endpoint)
            if len(tables) > 0 and t_name not in tables:
                logger.debug("skipping table '{}' due to filter".format(t_name))
                continue

            tbl = database[t_name]

            # TODO: in order support 'text' encoding add extra args field to
            #       handler.CMDS
            responses = sessions.send(endpoints, list(commands), encoding='json')

            for response in responses:
                hostaddr = response.host

                if response.status != "ok":
                    logger.warn(response.errored[0])
                    continue

                #print(type(response.responses))
                response = callback(response)

                if not isinstance(response, list):
                    response = [response]

                for item in response:
                    item = dict(item)

                    if not tbl.find_one(item):
                        tbl.insert_one({
                            "_dut": hostaddr,
                            "_timestamp": int(time.time()),
                            **item
                        })

refresh = gather

def _prepare_query(endpoints=None, query={}):
    endpoints = [sess.endpoint for sess in sessions.filter(endpoints)]

    if endpoints:
        query["_dut"] = { "$in": endpoints }

    return query

def find(table, endpoints=None, query={}):
    query = _prepare_query(endpoints, query)

    result = database[table].find(query)

    if result:
        result = list(result)

    return result

def find_one(table, endpoints=None, query={}):

    query = _prepare_query(endpoints, query)
    return database[table].find_one(query)
