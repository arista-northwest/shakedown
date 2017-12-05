# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import collections
import yaml
from pprint import pprint
from shakedown.util import to_list, merge



class _ConfigSection(collections.MutableMapping):
    def __init__(self):

        self._subscribers = []
        self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._validate(key, value)
        self._data[key] = value
        self._notify("SET", key, value)

    def __delitem__(self, key):
        del self._data[key]
        self._notify("DEL", key, None)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    @property
    def name(self):
        (_, name) = self.__class__.__name__.split("_")
        return name.lower().split('section')[0]

    def to_dict(self):
        return self._data

    def _notify(self, action, key, value):
        for cb in self._subscribers:
            cb({
                "section": self,
                "action": action,
                "key": key,
                "value": value
            })

    def _validate(self, key, value):
        pass

    def mount(self, callback):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

        return self

class _ConnectionsSection(_ConfigSection):
    pass

class _VarsSection(_ConfigSection):
    pass

class _TestsSection(_ConfigSection):
    pass

class Config(collections.MutableMapping):

    def __init__(self):

        self._config = {
            'vars': _VarsSection(),
            'connections': _ConnectionsSection(),
            'tests': _TestsSection()
        }

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __delitem__(self, key):
        del self._config[key]

    def __iter__(self):
        return iter(self._config)

    def __len__(self):
        return len(self._config)

    def load(self, file):
        with open(file, "r") as fh:
            data = yaml.load(fh.read())
            self._handle_config_data(data)

    def merge(self, data):
        data = yaml.load(data)
        self._handle_config_data(data)

    def _handle_config_data(self, data):
        _config = {}

        for section, _data in data.items():
            if not isinstance(_data, (list, dict)):
                raise ValueError("only sections at top level...")

            if section not in self._config:
                raise KeyError("Unknown section '{}'".format(section))

            self._config[section].update(_data)

    def to_dict(self):
        _config = {}
        for section, _data in self._config.items():
            _config[section] = _data.to_dict()
        #print(_config)
        return _config

    def dump(self, **kwargs):
        return yaml.dump(self.to_dict(),
                         **kwargs)

    to_yaml = dump

    def mount(self, section, callback):
        #print(section, handler)
        if section not in self._config:
            raise KeyError("ERROR: section '{}' does not exists".format(section))

        return self._config[section].mount(callback)

    def __repr__(self):
        return str(self.to_dict())

config = Config()
