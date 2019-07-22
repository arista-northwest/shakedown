# # -*- coding: utf-8 -*-
# # Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# # Arista Networks, Inc. Confidential and Proprietary.
#
# import pexpect
import sys
import time

import eapi
import pexpect
from shakedown import ssh

DEFAULT_EAPI_AUTH = ("admin", "")

class Session(object):

    def __init__(self):
        self._session = ssh.Session()
        self._opener = None

    def open(self, hostaddr, secret="root", eapi_auth=None):
        auth = ("root", secret)
        try:
            self._session.open(hostaddr, auth)
        except ssh.SshException:
            self.install(hostaddr, secret, eapi_auth)

        self._opener = (hostaddr, secret, eapi_auth)
        self._session.open(hostaddr, auth)

    def install(self, hostaddr, secret="root", eapi_auth=None):
        if not eapi_auth:
            eapi_auth = DEFAULT_EAPI_AUTH

        eapi_sess = eapi.Session(hostaddr, auth=eapi_auth)
        eapi_sess.send([
            "configure",
            "aaa root secret %s" % secret,
            "end"
        ])

    def send(self, *args, **kwargs):
        return self._session.send(*args, **kwargs)

    def reopen(self):
        hostaddr, secret, eapi_auth = self._opener
        self.open(hostaddr, secret, eapi_auth)

    def close(self):
        self._session.close()

    # def repave(self, config, startup=False):
    #     """overwrites running configuration"""

    #     repave_config = "/tmp/shakedown_repave_config"

    #     fd, path = tempfile.mkstemp()

    #     try:
    #         with os.fdopen(fd, 'w') as tmp:
    #             # do stuff with temp file
    #             tmp.write(config)
    #             tmp.close()
    #             self.copyfile(path, repave_config)
    #     finally:
    #         os.remove(path)

    #     self._session.send([
    #         "bash timeout 30 sudo chmod 644 %s" % repave_config,
    #     ])

    #     if startup == True:
    #         self._session.send([
    #             "copy startup-config repave-backup",
    #             "copy file:%s startup-config" % repave_config,
    #         ])
    #     else:
    #         self._session.send("configure replace file:%s")

    #     self._session.send(
    #         ["bash timeout 30 sudo rm -f %s" % repave_config])

    # def reimage(self, image):
    #     response = self.configure(["boot system %s" % image])[0]

    # def revert(self):
    #     """revert the running configuration the startup configuration"""
    #     self._session.send(r'configure replace startup-config')

    def reload(self, save=False, waitfor=0):
        if save:
            self._session.send(r'Cli -p 15 -c write')

        try:
            self._session.send(r'echo reload now | Cli -p 15')
            while self._session.alive:
                pass
        except pexpect.EOF:
            time.sleep(10)

        self._session.close()

        if waitfor > 0:
            t0 = time.time()
            while True:
                try:
                    self.reopen()
                    while True:
                        line = ("echo 'show logging last 30 seconds "
                                "| i SYSTEM_RESTARTED' | Cli -p 15")
                        output = self._session.send(line)

                        if "System restarted" in output:
                            sys.stdout.write("!\n")
                            sys.stdout.flush()
                            return

                        sys.stdout.write("?")
                        sys.stdout.flush()

                        if int(time.time() - t0) >= waitfor:
                            raise ValueError("Timeout exceeded")

                        time.sleep(5)

                except pexpect.EOF:
                    pass
                except pexpect.TIMEOUT:
                    pass
                except eapi.EapiHttpError:
                    pass

                sys.stdout.write(".")
                sys.stdout.flush()

                if int(time.time() - t0) >= waitfor:
                    raise ValueError("Timeout exceeded")

            time.sleep(10)

Backdoor = Session
