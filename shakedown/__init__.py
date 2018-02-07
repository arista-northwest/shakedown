# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

__version__ = "0.2.2"


#from . import env
import os

from . import config

_base_path = os.path.dirname(os.path.abspath(__file__))
_settings_path = os.path.join(_base_path, "settings.yml")
config.config.load(_settings_path)
