# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from .basic import BasicMagics
from .management import ManagementMagics

def load_ipython_extension(shell):
    '''Registers the skip magic when the extension loads.'''
    shell.register_magics(BasicMagics, ManagementMagics)
