# -*- coding: utf-8 -*-
# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from shakedown import ssh

def run(session, config, startup=False):
    """overwrites running configuration"""
    
    return "repaving..."
    # repave_config = "/tmp/shakedown_repave_config"

    # fd, path = tempfile.mkstemp()

    # try:
    #     with os.fdopen(fd, 'w') as tmp:
    #         # do stuff with temp file
    #         tmp.write(config)
    #         tmp.close()
    #         self.copyfile(path, repave_config)
    # finally:
    #     os.remove(path)

    # self._session.send([
    #     "bash timeout 30 sudo chmod 644 %s" % repave_config,
    # ])

    # if startup == True:
    #     self._session.send([
    #         "copy startup-config repave-backup",
    #         "copy file:%s startup-config" % repave_config,
    #     ])
    # else:
    #     self._session.send("configure replace file:%s")

    # self._session.send(
    #     ["bash timeout 30 sudo rm -f %s" % repave_config])
