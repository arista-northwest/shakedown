# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from collections import abc
import yaml
from shakedown.util import to_list, merge

SECTIONS = [
    'settings',
    'vars',
    'connections',
    'tests',
    'scout',
    'publishers',
    'backdoor'
]

class _ConfigSection(abc.MutableMapping):
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

    def mount(self, callback=None):
        if callback:
            if callback not in self._subscribers:
                self._subscribers.append(callback)

        return self

class Config(abc.MutableMapping):

    def __init__(self):
        self._store = None
        self.initialize()

    def __delitem__(self, key):
        del self._store[key]

    def __getitem__(self, key):
        return self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return str(self.to_dict())

    def __setitem__(self, key, value):
        self._store[key] = value

    def _handle_config_data(self, data):
        _config = {}

        for section, _data in data.items():

            if section not in self._store:
                raise KeyError("Unknown section '{}'".format(section))

            self._store[section].update(_data or {})

    def dump(self, **kwargs):
        return yaml.dump(self.to_dict(), **kwargs)

    def load(self, file):
        with open(file, "r") as fh:
            data = yaml.full_load(fh.read())
            self._handle_config_data(data)

    def merge(self, data):
        data = yaml.safe_load(data)
        self._handle_config_data(data)

    def mount(self, section, callback=None):
        if section not in self._store:
            raise KeyError("ERROR: section '{}' does not exists".format(section))

        return self._store[section].mount(callback)

    def initialize(self):
        self._store = { s: _ConfigSection() for s in SECTIONS }

    def to_dict(self):
        _config = {}
        for section, _data in self._store.items():
            _config[section] = _data.to_dict()
        return _config

    to_yaml = dump

config = Config()
