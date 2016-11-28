#
#

"""
Magic functions for Arista device testing
"""

# def skip(line, cell=None):
#     '''Skips execution of the current line/cell.'''
#     pass
#
# def load_ipython_extension(shell):
#     '''Registers the skip magic when the extension loads.'''
#     shell.register_magic_function(skip, 'line_cell')
#
# def unload_ipython_extension(shell):
#     '''Unregisters the skip magic when the extension unloads.'''
#     del shell.magics_manager.magics['cell']['skip']

import arcomm
import argparse
import re
from getpass import getpass, getuser

from IPython.core import magic_arguments
from IPython.core.display import display_pretty, display
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, on_off, needs_local_scope)

@magics_class
class ShakedownMagics(Magics):

    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)

    # @line_cell_magic
    # def sd(self, line, cell=None):
    #
    #     args = self._parse_line_cell(line, cell)
    #
    #     #parser = argparse.ArgumentParser()
    #     #parser.add_argument('-m', '--mute', action="store_true")
    #     #parser.add_argument('-c', '--capture', action="store_true")
    #
    #     cmd = args.pop(0)
    #
    #     response = getattr(self, "_sd" + cmd)(args, parser)
    #
    #     args = parser.parse_args(args)
    #
    #     return response

    # @magic_arguments.magic_arguments()
    # @magic_arguments.argument('hostname', nargs="*",
    #     help="""Host(s) to connect to""")
    # @magic_arguments.argument('-u', '--username',
    #     help="""Username for connection""")
    # @magic_arguments.argument('-p', '--password', default="",
    #     help="""Password for connection""")
    # @line_magic
    # def sdconnect(self, line):
    #
    #     args = magic_arguments.parse_argstring(self.sdconnect, line)
    #
    #     for hostname in args.hostname:
    #         if not args.username:
    #             args.username = getuser()
    #
    #         if not args.password:
    #             _prompt = "{}@{}'s password: ".format(args.username, hostname)
    #             args.password = getpass(_prompt) or ""
    #
    #         conn = arcomm.connect(hostname, creds=(args.username, args.password))
    #         self._connections[hostname] = conn
    #
    #     #return self._connections
    #
    # @magic_arguments.magic_arguments()
    # @magic_arguments.argument('connections', nargs="*",
    #     help="""Select existing connection by hostname""")
    # @magic_arguments.argument('-e', '--encoding', default="text",
    #     choices=["text", "json"],
    #     help="""Specify output encoding: json or text""")
    # @magic_arguments.argument('-c', '--command',
    #     help="""Commands to send to host""")
    # @magic_arguments.argument('--no-display', action="store_true",
    #     help="""Skip printing responses""")
    # @magic_arguments.argument('--capture', action="store_true", default=True,
    #     help="""Specify whether to return responses [default: True]""")
    # @line_cell_magic
    # def sdsends(self, line, cell=None):
    #
    #     args = magic_arguments.parse_argstring(self.sdsends, line)
    #
    #     responses = []
    #     if args.command:
    #         args.command = [args.command]
    #     else:
    #         cell_cmds = [cmd for cmd in cell.splitlines()]
    #         args.command = cell_cmds
    #
    #     commands = [re.sub("(?:^\"|\"$)", "", cmd) for cmd in args.command]
    #
    #     for name in args.connections:
    #         conn = self._connections.get(name, None)
    #         if not conn:
    #             raise ValueError("Connection to '{}' does not exist".format(conn))
    #         response = conn.send(commands, encoding=args.encoding)
    #         responses.append(response)
    #
    #         if not args.no_display:
    #             # if args.encoding == "text":
    #             #     print(response.to_yaml())
    #             # else:
    #             #     print(response)
    #             print(response)
    #
    #     return responses

    # def _parse_line_cell(self, line, cell):
    #     args = []
    #     if cell is None:
    #         # split arguments, preserve spaces within "s
    #         args = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
    #         # remove surrounding ""s
    #         args = [re.sub("(?:^\"|\"$)", "", arg) for arg in args]
    #     else:
    #         args = self._parse_line_cell(line, cell=None)
    #         args += cell.splitlines()
    #
    #     return args

def load_ipython_extension(shell):
    '''Registers the skip magic when the extension loads.'''
    shell.register_magics(ShakedownMagics)

def unload_ipython_extension(shell):
    '''Unregisters the skip magic when the extension unloads.'''
    pass
