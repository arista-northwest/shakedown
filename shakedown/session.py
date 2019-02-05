# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import asyncio
import collections
import functools
import re
import time

import eapi

from shakedown.util import to_list, merge
from shakedown.config import config

class SessionError(Exception):
    pass

class Session(collections.MutableMapping):
    def __init__(self, endpoint, tags=[], **kwargs):

        self.__dict__["_store"] = {
            "endpoint": endpoint,
            "tags": tags
        }
        self.__dict__["_store"].update(kwargs)

        self.eapi_params = kwargs

    def __getattr__(self, item):
        return self._store[item]

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
        self._sessions = collections.OrderedDict()

    clear = reset

    def chamber(self, endpoint, config):
        """prepare to connect. but wait for first send"""

        tags = []

        if "tags" in config and not isinstance(config["tags"], (list, tuple)):
                config["tags"] = tags.split(",")

        #self._sessions[endpoint] = dict(**config)
        self._sessions[endpoint] = Session(endpoint, **config)

    def filter(self, patterns):
        """filter connections for hostname or tags"""

        filtered = []

        patterns = [re.compile(pat) for pat in to_list(patterns)]

        #for endpoint, item in self._sessions.items():
        for ep, session in self._sessions.items():
            # params, tags = item
            config = session.eapi_params

            keys = [session.endpoint] + session.tags

            for pattern in patterns:
                for f in filter(pattern.match, keys):
                    if session not in filtered:
                        filtered.append(session)

        return filtered #list(filtered.items())

    def remove(self, endpoints):
        endpoints = to_list(endpoints)
        defunct = []
        for session in self.filter(endpoints):
            defunct.append(session.hostname)

        for hostname in defunct:
            del self._sessions[hostname]

    def send(self, *args, **kwargs):
        """This function is monkey-patched by a fixture, so we need to maintain
        access to the 'real' :meth:`SessionManager._send` method for internal
        use"""
        return self._send(*args, **kwargs)

    def _send(self, endpoints, commands, callback=None, **kwargs):

        responses = []
        filtered = self.filter(endpoints)
        commands = to_list(commands)

        kwargs.setdefault("encoding", "text")

        loop = asyncio.get_event_loop()

        for response in loop.run_until_complete(_asend(filtered, commands, **kwargs)):
            # if raise_for_error:
            response.raise_for_error()

            if callback:
                callback(response)
            responses.append(response)

        return responses

    execute = send

async def _asend(filtered, commands, **kwargs):
    loop = asyncio.get_event_loop()

    tasks = []

    def _send_until(sess, commands, **kwargs):

        # default will match on anything
        condition = r".*"
        timeout = 30
        sleep = 1
        exclude = None

        start_time = time.time()
        check_time = start_time

        # handle the 'until' arg. it can be a dict...
        if "until" in kwargs:
            until = kwargs["until"]
            del(kwargs["until"])

            if isinstance(until, dict):
                if "condition" not in until:
                    raise ValueError("'condition' expected")
                condition = until["condition"]
                timeout = until.get("timeout") or timeout
                sleep = until.get("sleep") or sleep
                exclude = until.get("exclude")
            else:
                condition = until

        while (check_time - timeout) < start_time:

            response = sess.send(commands, **kwargs)
            match = re.search(condition, "\n".join([r.text for r in response]))

            if exclude:
                if not match:
                    return response
            elif match:
                return response

            time.sleep(sleep)

            check_time = time.time()

        raise ValueError("condition did not match withing timeout period")

    for session in filtered:
        sess = eapi.Session(session.endpoint, **session.eapi_params)
        part = functools.partial(_send_until, sess, commands, **kwargs)
        tasks.append(loop.run_in_executor(None, part))

    completed, pending = await asyncio.wait(tasks)

    return [task.result() for task in completed]

sessions = SessionManager()
