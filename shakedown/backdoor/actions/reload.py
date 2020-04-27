# -*- coding: utf-8 -*-
# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import time

import pexpect

from shakedown import ssh

def run(session, save=False, waitfor=0):
    if save:
        session.send(r'Cli -p 15 -c write')

    try:
        session.send(r'echo reload now | Cli -p 15')
        while session.alive:
            pass
    except ssh.SshSessionClosedException:
        pass
    except pexpect.EOF:
        pass

    time.sleep(30)
    
    session.close()

    if waitfor > 0:
        t0 = time.time()
        while True:
            try:
                session.reopen()
                while True:
                    line = ("echo 'show logging last 30 seconds "
                            "| i SYSTEM_RESTARTED' | Cli -p 15")
                    output = session.send(line)

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
            except ssh.SshSessionClosedException:
                pass

            sys.stdout.write(".")
            sys.stdout.flush()

            if int(time.time() - t0) >= waitfor:
                raise ValueError("Timeout exceeded")

        time.sleep(10)