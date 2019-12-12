# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Wrapper for TinyMongoClient and TinyDB

TODO: all sessions and config will to be stored here...
"""
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinymongo import TinyMongoDatabase, TinyMongoCollection

class Database(TinyMongoDatabase):

    def __init__(self, *args, **kwargs):

        # use `MemoryStorage` by default if no path is given
        if len(args) == 0:
            kwargs.setdefault("storage", MemoryStorage)

        self.tinydb = TinyDB(*args, **kwargs)

    def __getattr__(self, name):
        """Gets a new or existing collection"""
        return self[name]

    def __getitem__(self, name):
        """Gets a new or existing collection"""
        return Collection(name, self)

    @property
    def collections(self):
        """Get a list of all the collection names in this database"""
        return self.collection_names()

    tables = collections


class Collection(TinyMongoCollection):
    pass
