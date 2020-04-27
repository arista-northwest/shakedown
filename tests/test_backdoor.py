# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os

from shakedown import backdoor

SSH_HOST = os.environ.get("SSH_HOST", "veos1")
SSH_USER = os.environ.get("EAPI_USER", "admin")
SSH_PASS = os.environ.get("EAPI_PASS", "")
BACKDOOR_SECRET = os.environ.get("BACKDOOR_SECRET", "censored")

def test_backdoor():
    sess = backdoor.Session()
    sess.open(SSH_HOST, secret=BACKDOOR_SECRET, auth=(SSH_USER, SSH_PASS))
    sess.send("uname -a")

def test_repave():
    sess = backdoor.Session()
    sess.open(SSH_HOST, secret=BACKDOOR_SECRET, auth=(SSH_USER, SSH_PASS))

    #sess.do("repave", config="")

def test_reload():
    sess = backdoor.Session()
    sess.open(SSH_HOST, secret=BACKDOOR_SECRET, auth=(SSH_USER, SSH_PASS))

    sess.do("reload", waitfor=3600)
