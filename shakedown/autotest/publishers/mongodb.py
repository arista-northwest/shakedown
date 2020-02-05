# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json

from datetime import datetime

try:
    from pymongo import MongoClient
except ImportError:
    pass

from shakedown.config import config


def render(data):
    data["_timestamp"] = datetime.utcnow()
    return json.dumps(data)


def save(data, path):
    params = []
    if "publishers" in config:
        if "mongodb" in config["publishers"]:
            params = config["publishers"]["mongodb"]

    host = params.get("host", "localhost")
    port = params.get("port", 27017)

    client = MongoClient(host, port)
    db = client.shakedown
    collection = db.test_results
    collection.insert(render(data))