# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os

from shakedown import ssh

SSH_HOST = os.environ.get("SSH_HOST", "veos-2")
SSH_USER = os.environ.get("SSH_USER", "admin")
SSH_PASS = os.environ.get("SSH_PASS", "")
SSH_ROOT_PASS = os.environ.get("SSH_ROOT_PASS", "root")

def test_ssh():
    sess = ssh.Session()
    sess.open(SSH_HOST, auth=(SSH_USER, SSH_PASS))

    sess.send("show version")

def test_root():
    sess = ssh.Session()
    sess.open(SSH_HOST, auth=("root", SSH_ROOT_PASS))

    sess.send("uname -a")

def test_copy():
    ssh.copy("tests/testfile",
             "%s@%s:/mnt/flash/testfile" % (SSH_USER, SSH_HOST), password="")

    ssh.copy("%s@%s:/mnt/flash/testfile" % (SSH_USER, SSH_HOST),
             "tests/testfile", password="")


def test_reopen():
    sess = ssh.Session()
    sess.open(SSH_HOST, auth=("root", SSH_ROOT_PASS))
    sess.send("uname -a")
    sess.reopen()
    sess.send("uname -a")

def test_background():
    with ssh.Background(SSH_HOST, (SSH_USER, SSH_PASS), "bash sleep 5; uname -a") as bk:
        print("started in background...")

    for result in bk:
        print(result)


