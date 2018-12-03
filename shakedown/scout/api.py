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

_cached = []
database = Database()

def gather(endpoints=r".*", tables=[]):
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
            responses = sessions._send(endpoints, list(commands), encoding='json')

            for response in responses:
                hostaddr = response.host

                if response.status != "ok":
                    logger.warning(response.errored)
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

def _get_handler(table):
    for handler_name, handler in handlers.handlers:
        for key, cmds, callback in handler.CMDS:
            _table = ".".join([handler_name, key])
            if _table == table:
                return (database[table], cmds, callback)

    raise ValueError("table '{}' not found".format(table))

def _get_endpoints(filter):
    return [sess.endpoint for sess in sessions.filter(filter)]

def _prepare_query(endpoints=None, query={}):
    if endpoints:
        query["_dut"] = { "$in": endpoints }

    return query

def _get_cache_key(table, endpoint):
    return "::".join([table, endpoint])

def _get_not_cached(table, endpoints):
    return [ep for ep in endpoints if _get_cache_key(table, ep) not in _cached]

def _set_cached(table, endpoint):
    key = _get_cache_key(table, endpoint)

    if key not in _cached:
        _cached.append(key)

def _cache(table, endpoints):
    endpoints = _get_not_cached(table, endpoints)
    if not endpoints:
        return
    table, commands, callback = _get_handler(table)
    responses = sessions._send(endpoints, list(commands), encoding='json')

    for response in responses:
        hostaddr = response.host

        if response.status != "ok":
            logger.warning(response.errored)
            continue

        response = callback(response)

        if not isinstance(response, list):
            response = [response]

        for item in response:
            item = dict(item)

            if not table.find_one(item):
                table.insert_one({
                    "_dut": hostaddr,
                    "_timestamp": int(time.time()),
                    **item
                })
            else:
                table.update_one(item, {
                    "_dut": hostaddr,
                    "_timestamp": int(time.time()),
                    **item
                })

        _set_cached(str(table), hostaddr)

def find(table, endpoints=None, query={}):
    endpoints = _get_endpoints(endpoints)

    _cache(table, endpoints)

    query = _prepare_query(endpoints, query)
    result = database[table].find(query)

    if result:
        result = list(result)

    return result

def find_one(table, endpoints=None, query={}):
    endpoints = _get_endpoints(endpoints)

    _cache(table, endpoints)

    query = _prepare_query(endpoints, query)
    return database[table].find_one(query)
