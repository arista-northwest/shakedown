# -*- coding: utf-8 -*-
# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
"""Provide root access via SSH to an Arista switch

Aristas have a feature that enables user to login as 'root'.  This feature is
useful for testing and prevents getting locked out do to AAA misconfiguration.
When logging in as root the operator is dropped into a bash shell instead of
the standard CLI

  Typical usage example:
   
    from shakedown import backdoor
    sess = backdoor.Session()   
    sess.open("switch", secret="s3cr3t", auth=("admin", "p$ssw0rd"))
    response = sess.send("uname -a")
"""

import sys
import time
import importlib

from functools import partial

import pexpect

from shakedown import ssh

DEFAULT_SSH_AUTH = ("admin", "")


class Session(object):
    """Connect to an arista switch using the root user.  This bypasses AAA settings."""
    def __init__(self):
        self._session = ssh.Session()
        self._opener = None

    def __getattr__(self, attr):
        mod = importlib.import_module("shakedown.backdoor.actions.%s" % attr)

        return partial(mod.run, self)

    def do(self, command, *args, **kwargs):
        mod = importlib.import_module("shakedown.backdoor.actions.%s" %
                                      command)
        return mod.run(self, *args, **kwargs)

    def open(self, hostaddr, secret="root", auth=None):
        """Opens a new backdoor session"""
        _opener = partial(self._session.open, hostaddr, ("root", secret))

        try:
            _opener()
        except ssh.SshException:
            self.install(hostaddr, auth, secret)
            _opener()

        self._opener = _opener

    def install(self, hostaddr, auth=None, secret="root"):
        """Installs the root user"""

        if not auth:
            auth = DEFAULT_SSH_AUTH

        sess = ssh.Session()
        sess.open(hostaddr, auth=auth)
        sess.send("configure")
        sess.send("aaa root secret %s" % secret)
        sess.send("end")
        sess.close()

    def send(self, *args, **kwargs):
        """Send a command"""

        return self._session.send(*args, **kwargs)

    def reopen(self):
        """Re-open a session"""

        self._opener()

    def close(self):
        """Close the session, can be reopened later with `reopen`"""
        self._session.close()


Backdoor = Session
