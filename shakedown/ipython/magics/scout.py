# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Magic functions for Arista device testing
"""

import sys
import warnings
import jinja2
import json

from IPython.core import magic_arguments
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)

from shakedown.config import config
from shakedown.session import sessions
from shakedown.scout import api as scout
from shakedown import util

@magics_class
class ScoutMagics(Magics):
    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)

        self.shell.user_ns["_sdscout"] = scout

    #     scout.gather()
    #
    # @needs_local_scope
    # @magic_arguments.magic_arguments()
    # @magic_arguments.argument("command",
    #     help="Run a scout command (find , find_one or gather)")
    # @magic_arguments.argument("table", nargs="?",
    #     help="Scout table name")
    # @magic_arguments.argument("filter",  nargs="?", default=".*",
    #     help="Filter connections (DUT)")
    # @magic_arguments.argument("query", nargs="*", default=["{}"],
    #     help="Query string (mongo compatible)")
    # @line_magic
    # def sdscout(self, line='', local_ns=None):
    #     args = magic_arguments.parse_argstring(self.sdscout, line)
    #     resp = getattr(scout, args.command)(args.table, args.filter,
    #                                         json.loads(" ".join(args.query)))
    #     util.pplush(resp)
