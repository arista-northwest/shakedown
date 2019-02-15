# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os

from shakedown import backdoor

SSH_HOST = os.environ.get("SSH_HOST", "veos-1")
EAPI_USER = os.environ.get("EAPI_USER", "admin")
EAPI_PASS = os.environ.get("EAPI_PASS", "")
SSH_ROOT_PASS = os.environ.get("SSH_ROOT_PASS", "butthole")

def test_backdoor():
    sess = backdoor.Session()
    sess.open(SSH_HOST, secret=SSH_ROOT_PASS, eapi_auth=(EAPI_USER, EAPI_PASS))
    sess.send("uname -a")

def test_reload():
    sess = backdoor.Session()
    sess.open(SSH_HOST, secret=SSH_ROOT_PASS, eapi_auth=(EAPI_USER, EAPI_PASS))

    sess.reload(waitfor=3600)
