# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Magic functions for Arista device testing
"""

import sys
import warnings
import jinja2

from IPython.core import magic_arguments
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)

from shakedown.config import config
from shakedown.session import sessions
from shakedown import util

@magics_class
class BasicMagics(Magics):

    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)

        self.shell.user_ns["_sdconfig"] = config

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("file", nargs="*",
        help="Load a YAML file from path")
    @line_cell_magic
    def sdconfig(self, line='', cell=None, local_ns=None):
        result = None

        args = magic_arguments.parse_argstring(self.sdconfig, line)

        for file in args.file:
            config.load(file)

        if cell:
            config.merge(cell)

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Host(s) to connect to")
    @magic_arguments.argument("-a", "--askpass", action="store_true",
        help="Force prompt for password.")
    @magic_arguments.argument("-c", "--clear", action="store_true",
        help="Clear all connections")
    @magic_arguments.argument("-s", "--section",
        help="Read from configuration section")
    @line_cell_magic
    def sdconnect(self, line, cell=None, local_ns={}):
        warnings.warn("`sdconnect` is deprecated. connections are automatically made from `sdconfig`")


    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Connections to use")
    # @magic_arguments.argument("-t", "--test", action="append")
    @magic_arguments.argument("-e", "--encoding", default="text",
        choices=["text", "json"],
        help="Specify output encoding: json or text")
    @magic_arguments.argument("-o", "--output-file",
        help="sendoutput to specified file")
    @cell_magic
    def sdsend(self, line, cell=None, local_ns={}):

        args = magic_arguments.parse_argstring(self.sdsend, line)

        commands = []
        responses = []

        template = jinja2.Template(cell)
        commands = template.render(config).splitlines()

        for response in sessions.send(args.endpoints, commands, encoding=args.encoding):
            if args.output_file:
                util.plush("Writing output to {}".format(args.output_file))
                with open(args.output_file, "w") as fh:
                    fh.write(str(response))
            else:
                util.plush(str(response))
