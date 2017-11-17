# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import collections
import yaml
import warnings
import http.client

from pprint import pprint
from shakedown.util import to_list, merge
from shakedown.config import config

from requests.sessions import ChunkedEncodingError

import arcomm
# DEFAULT_TRANSPORT = "eapi+http"
# DEFAULT_USERNAME = "admin"
# DEFAULT_PASSWORD = ""

class SessionError(Exception):
    pass

class SessionManager:

    def __init__(self):

        # stores session objects. assigned in `reset`
        self._sessions = None

        self.reset()

        self._config = config.mount("connections", self._handler)

    def _handler(self, data):
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

            #del config["tags"]

        #session = arcomm.Session(endpoint, **config)

        self._sessions[endpoint] = (config, tags)

    def filter(self, keys):
        """filter connections for hostname or tags"""

        filtered = []
        # endpoints = []

        keys = to_list(keys)

        for endpoint, item in self._sessions.items():
            params, tags = item

            # look for matching hostname or common tags
            if endpoint in keys or set(keys) & set(tags):
                filtered.append((endpoint, params))

        return filtered

    def remove(self, endpoints):
        endpoints = to_list(endpoints)
        defunct = []
        for session in self.filter(endpoints):
            #session.close()
            defunct.append(session.hostname)

        for hostname in defunct:
            del self._sessions[hostname]

    def send(self, endpoints, commands, **kwargs):
        """sends commands to endpoints"""

        filtered = self.filter(endpoints)
        #print("ENDPOINTS:", filtered)
        pool = arcomm.batch(filtered, commands, **kwargs)

        for response in pool:
            yield response
        # for session in self.filter(endpoints):
        #     response = None
        #     if not session._conn:
        #         session.connect()
        #
        #     try:
        #         response = session.send(commands, **kwargs)
        #     except ChunkedEncodingError as e:
        #         # this occurs when a command causes the switch to go away
        #         warnings.warn("response interrupted")
        #         pass
        #
        #     yield response


sessions = SessionManager()

def main():
#     config.merge("""\
# global:
#     vrf: management
#     upgrade: "flash:EOS-4.19.1F.swi"
#     downgrade: "flash:EOS-4.18.3.1F.swi"
#
# duts:
#   veos-01:
#     creds: [ admin, "" ]
#     protocol: eapi+http
#     tags: [ dut, swan ]
#
#   veos-02:
#     creds: [ admin,  "" ]
#     tags: [ sdut, swan ]
#
# tests:
#     downgrade:
#         testrail_case_id: C12345
#
#
# """)
    config.load("notebooks/config.yml")

    for response in sessions.send("swan", "show hostname"):
        print(response)

    # sessions.remove("veos-01")
    #
    # for response in sessions.send("swan", "show hostname"):
    #     print(response)

if __name__ == '__main__':
    main()
