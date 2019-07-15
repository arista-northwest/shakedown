# -*- coding: utf-8 -*-
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from shakedown import util

def test_column():
    data = """a b c d e f
a b c d e f
a b c d e f
"""
    # results = util.column(data, 2)
    assert util.column(data, 2) == "c\nc\nc"

def test_grep():
    data = """a b c d e x
a b c d e y
a b c d z
"""
    assert util.grep(r"y", data) == "a b c d e y"

def test_indentblock():
    data = """a b c d e f
a b c d e f
a b c d e f"""

    result = """    a b c d e f
    a b c d e f
    a b c d e f"""

    assert util.indentblock(data, 4) == result

def test_to_list():
    pass

def test_merge():
    pass

def test_mkdir():
    pass

def test_plush():
    pass

def test_unzip():
    pass

def test_udiff():
    pass

def test_uniq():
    pass
