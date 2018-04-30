# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import asyncio
import collections
import functools
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

class Session(collections.MutableMapping):
    def __init__(self, endpoint, creds, protocol="eapi+http", tags=[]):

        self.__dict__["_store"] = {
            "endpoint": endpoint,
            "creds": creds,
            "protocol": protocol,
            "tags": tags
        }

    @property
    def config(self):
        return {
            key:value
            for (key,value) in self.items()
            if key not in ["tags", "endpoint"]
        }

    def __getattr__(self, item):
        # try:
        return self._store[item]
        # except KeyError:
        #     raise AttributeError('asd')
    def __getitem__(self, item):
        return self._store[item]

    def __setattr__(self, item, value):
        self._store[item] = value

    def __setitem__(self, item, value):
        self._store[item] = value

    def __delitem__(self, item):
        del(self._store[item])

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

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
        self._sessions = [] #collections.OrderedDict()

    clear = reset

    def chamber(self, endpoint, config):
        """prepare to connect. but wait for first send"""

        tags = []

        if "tags" in config and not isinstance(config["tags"], (list, tuple)):
                config["tags"] = tags.split(",")

        #self._sessions[endpoint] = dict(**config)
        self._sessions.append(Session(endpoint, **config))

    def filter(self, patterns):
        """filter connections for hostname or tags"""

        filtered = []

        patterns = [re.compile(pat) for pat in to_list(patterns)]

        #for endpoint, item in self._sessions.items():
        for session in self._sessions:
            # params, tags = item
            config = session.config

            # copy tags don't get a reference
            keys = list(session.tags)

            keys.insert(0, session.endpoint)

            for pattern in patterns:
                for f in filter(pattern.match, keys):
                    #filtered[endpoint] = config
                    filtered.append(session)

        return filtered #list(filtered.items())

    def remove(self, endpoints):
        endpoints = to_list(endpoints)
        defunct = []
        for session in self.filter(endpoints):
            defunct.append(session.hostname)

        for hostname in defunct:
            del self._sessions[hostname]

    def send(self, endpoints, commands, raise_for_error=False, **kwargs):

        responses = []
        filtered = self.filter(endpoints)

        until = kwargs.get("until")

        if until:
            del(kwargs["until"]) # 'until' is not recognized by arcomm
            kwargs["condition"] = until
            kwargs.setdefault("exclude", False)
            kwargs.setdefault("timeout", 30)
            kwargs.setdefault("delay", 1)
            kwargs.setdefault("method", "execute_until")

        loop = asyncio.get_event_loop()

        for response in loop.run_until_complete(_asend(filtered, commands,
                                                       **kwargs)):
            if raise_for_error:
                response.raise_for_error()
            responses.append(response)

        return responses

    execute = send

sessions = SessionManager()

async def _asend(filtered, commands, method="execute", *args, **kwargs):
    loop = asyncio.get_event_loop()

    tasks = []

    for session in filtered:
        sess = arcomm.Session(session.endpoint, **session.config)
        part = functools.partial(getattr(sess, method), commands, **kwargs)
        tasks.append(loop.run_in_executor(None, part))

    completed, pending = await asyncio.wait(tasks)

    return [t.result() for t in completed]
