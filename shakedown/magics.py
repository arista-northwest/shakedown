#
#

"""
Magic functions for Arista device testing
"""

import arcomm
import collections
import re
import sys
import warnings
import yaml

import jinja2

from getpass import getpass, getuser

from IPython.core import magic_arguments
from IPython.core.display import display_pretty, display
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)

@magics_class
class ShakedownMagics(Magics):

    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)
        self._connections = collections.OrderedDict()

    def _find_connections(self, key):
        connections = []
        for pkey, item in self._connections.items():
            if key == pkey or key in item["tags"]:
                connections.append(item["conn"])
        return connections

    def _preparse_endpoint(self, endpoint):
        tags = []
        if "|" in endpoint:
            endpoint, tags = endpoint.split("|")
            tags = tags.split(",")

        return endpoint, tags

    @needs_local_scope
    @cell_magic
    def sdconfig(self,line='', cell=None, local_ns=None):
        self.shell.user_ns["_sdconfig"] = yaml.load(cell)

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Host(s) to connect to")
    @magic_arguments.argument("-a", "--askpass", action="store_true",
        help="Force prompt for password.")
    @magic_arguments.argument("-c", "--clear", action="store_true",
        help="Clear all connections")
    @line_cell_magic
    def sdconnect(self, line, cell=None, local_ns={}):
        args = magic_arguments.parse_argstring(self.sdconnect, line)

        if args.clear:
            self._connections = collections.OrderedDict()

        config = self.shell.user_ns.get("_sdconfig", {})
        endpoints = args.endpoints

        if cell:
            endpoints += cell.splitlines()

        template = jinja2.Template("\n".join(endpoints))
        endpoints = template.render(config).splitlines()

        for endpoint in endpoints:
            #
            endpoint, tags = self._preparse_endpoint(endpoint)
            conn = arcomm.connect(endpoint, askpass=args.askpass)
            tags.append(conn.hostname)
            self._connections[conn.hostname] = {"conn": conn, "tags": tags}

        return self._connections

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Connections to use")
    @magic_arguments.argument("-e", "--encoding", default="text",
        choices=["text", "json"],
        help="Specify output encoding: json or text")
    @line_cell_magic
    def sdsend(self, line, cell=None, local_ns={}):

        args = magic_arguments.parse_argstring(self.sdsend, line)

        config = self.shell.user_ns.get("_sdconfig", {})

        commands = []
        responses = []

        template = jinja2.Template(cell)
        commands = template.render(config).splitlines()

        for key in args.endpoints:
            connections = self._find_connections(key)

            for conn in connections:
                if commands:
                    response = conn.send(commands, encoding=args.encoding)

                    print(response)
                    sys.stdout.flush()

                    responses.append(response)

        return responses

def load_ipython_extension(shell):
    '''Registers the skip magic when the extension loads.'''
    shell.register_magics(ShakedownMagics)

def unload_ipython_extension(shell):
    '''Unregisters the skip magic when the extension unloads.'''
    pass
