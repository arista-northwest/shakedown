# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import time

from IPython.core import magic_arguments
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)

from shakedown.config import config
from shakedown.session import sessions
from shakedown import util

from arcomm.exceptions import ConnectFailed, ExecuteFailed

@magics_class
class ManagementMagics(Magics):

    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Host(s) to connect to")
    @line_magic
    def sdversion(self, line=''):
        args = magic_arguments.parse_argstring(self.sdversion, line)
        shell = self.shell

        for response in sessions.send(args.endpoints, ["show version"]):
            util.plush(response)

    # @magic_arguments.magic_arguments()
    # @magic_arguments.argument("endpoints", nargs="*",
    #     help="Host(s) to connect to")
    # @line_magic
    # def sdreload(self, line=''):
    #     args = magic_arguments.parse_argstring(self.sdversion, line)
    #     cmd = "bash timeout 30 $(sleep 1; sudo reboot) &"
    #
    #     for response in sessions.send(args.endpoints, [cmd]):
    #         pass
    #
    #     time.sleep(10)
    #
    #     filtered = sessions.filter(args.endpoints)
    #
    #     util.plush("polling {}\n".format(str([s[0] for s in filtered])))
    #
    #     width = 0
    #     while filtered:
    #         for endpoint, params in filtered:
    #             if width >= 80:
    #                 width = 0
    #                 util.plush("\n")
    #             try:
    #
    #                 for response in sessions.send([endpoint], ["show uptime"],
    #                                               timeout=1):
    #                     pass
    #                 util.plush("+")
    #                 filtered.remove((endpoint, params))
    #             except ConnectFailed as e:
    #                 util.plush(".")
    #                 pass
    #
    #             width += 1
    #
    #     time.sleep(1)
