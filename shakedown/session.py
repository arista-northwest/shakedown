# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import collections
import yaml
import warnings
import http.client
import re
from pprint import pprint
from shakedown.util import to_list, merge
from shakedown.config import config

from requests.sessions import ChunkedEncodingError

import arcomm

class SessionError(Exception):
    pass

class SessionManager:

    def __init__(self):

        # stores session objects. assigned in `reset`
        self._sessions = None

        self.reset()

        self._config = config.mount("connections", self._handle_notifications)

    def _handle_notifications(self, data):
        """handler is blocking should return immediately"""

        action = data["action"]
        if action == "SET":
            self.chamber(data["key"], data["value"])
        elif action == "DEL":
            self.close(data["key"])

    def reset(self):
        self._sessions = collections.OrderedDict()

    clear = reset

    def chamber(self, endpoint, config):
        """prepare to connect. but wait for first send"""

        tags = []

        if "tags" in config:
            tags = config["tags"]

            if not isinstance(tags, (list, tuple)):
                tags = tags.split(",")

        self._sessions[endpoint] = (config, tags)

    def filter(self, keys):
        """filter connections for hostname or tags"""

        filtered = {}

        keys = to_list(keys)

        for endpoint, item in self._sessions.items():
            params, tags = item

            tags_ = list(tags)
            tags_.insert(0, endpoint)

            for key in keys:
                pattern = re.compile(key)
                for f in filter(pattern.match, tags_):
                    filtered[endpoint] = params

        return list(filtered.items())

    def remove(self, endpoints):
        endpoints = to_list(endpoints)
        defunct = []
        for session in self.filter(endpoints):
            defunct.append(session.hostname)

        for hostname in defunct:
            del self._sessions[hostname]

    def send(self, endpoints, commands, raise_for_error=False, **kwargs):
        """sends commands to endpoints"""
        responses = []
        filtered = self.filter(endpoints)

        pool = arcomm.batch(filtered, commands, **kwargs)

        for response in pool:
            if raise_for_error:
                response.raise_for_error()
            responses.append(response)

        return responses

sessions = SessionManager()
