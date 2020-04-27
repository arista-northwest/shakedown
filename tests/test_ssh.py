# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os

from shakedown import ssh

SSH_HOST = os.environ.get("SSH_HOST", "veos3")
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
        pass

    for result in bk:
        print(result)


def test_input():
    message = "test_input_string"
    sess = ssh.Session()
    sess.open(SSH_HOST, auth=(SSH_USER, SSH_PASS))
    sess.send("bash")
    response = sess.send("read -p \"test_input:\" TEST_INPUT && echo $TEST_INPUT", prompt=r'test_input:', input=message)
    
    assert response.splitlines()[-1] == message