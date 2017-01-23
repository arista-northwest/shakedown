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
import re
import jinja2

from getpass import getpass, getuser

from IPython.core import magic_arguments
from IPython.core.display import display_pretty, display
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)
from IPython.utils.capture import capture_output
from io import StringIO

DEFAULT_TRANSPORT = 'eapi+http'
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = None

def _merge(destination, source):
    for (key, value) in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            _merge(value, node)
        elif isinstance(value, (tuple, list)):
            if key not in destination:
                destination[key] = []
            destination[key] += value
        else:
            destination[key] = value

    return destination

class OutputCap(object):

    def __init__(self):
        self._stdout = None
        self._sys_stdout = None

    @property
    def stdout(self):
        return self._stdout.getvalue()

    def __enter__(self):
        self._sys_stdout = sys.stdout
        sys.stdout = self._stdout = StringIO()
        return self

    def __exit__(self, *exc):
        sys.stdout = self._sys_stdout


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

    def _handle_tags(self, tags):
        if isinstance(tags, (list, tuple)):
            tags = ",".join(tags)

        return tags

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("-f", "--file",
        help="Load a YAML file from path")
    @line_cell_magic
    def sdconfig(self, line='', cell=None, local_ns=None):
        result = None
        args = magic_arguments.parse_argstring(self.sdconfig, line)

        config = {}

        if args.file:
            with open(args.file, "r") as cfh:
                config = yaml.load(cfh.read())

        if cell:
            config = _merge(config, yaml.load(cell))

        self.shell.user_ns["_sdconfig"] = config

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

        args = magic_arguments.parse_argstring(self.sdconnect, line)

        if args.clear:
            self._connections = collections.OrderedDict()

        config = self.shell.user_ns.get("_sdconfig", {})

        endpoints = args.endpoints or []

        if args.section:
            section = args.section

            try:
                duts = config[section]
            except KeyError as esc:
                raise ValueError("Invalid config section: {}".format(section))

            for dut in duts:
                transport = dut.get("transport") or DEFAULT_TRANSPORT
                username = dut.get("username") or DEFAULT_USERNAME
                password = dut.get("password", DEFAULT_PASSWORD)
                hostname = dut.get("hostname")

                if not hostname:
                    raise ValueError("'hostname' parameter is required")

                tags = self._handle_tags(dut.get("tags"))
                ep = "{}://{}:{}@{}|{}".format(transport, username, password,
                                               hostname, tags)

                endpoints.append(ep)

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

        self.shell.user_ns["_sdconnections"] = self._connections
        #return self._connections

    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("endpoints", nargs="*",
        help="Connections to use")
    @magic_arguments.argument("-t", "--test", action="append")
    @magic_arguments.argument("-e", "--encoding", default="text",
        choices=["text", "json"],
        help="Specify output encoding: json or text")

    @cell_magic
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
                    if args.test:
                        self._test_responses(args.test, response.responses)
                    print(response)
                    sys.stdout.flush()

                    responses.append(response)

        self.shell.user_ns["_sdresponses"] = responses
        return responses

    def _test_responses(self, patterns, responses):
        match = None

        for response in responses:
            for pattern in patterns:
                for line in str(response).splitlines():
                    match = re.search(pattern, line)
                    if match:
                        break

        if not match:
            sys.stderr.write("Response did not match any patterns")


def load_ipython_extension(shell):
    '''Registers the skip magic when the extension loads.'''
    shell.register_magics(ShakedownMagics)

def unload_ipython_extension(shell):
    '''Unregisters the skip magic when the extension unloads.'''
    pass
