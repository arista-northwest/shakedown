# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pytest

from shakedown.autotest import pytest_plugin, fixtures

def main():
    """Main routing. provides entrypoint hook to setuputils"""
    import sys
    pytest.main(sys.argv[1:], plugins=[pytest_plugin, fixtures])

if __name__ == "__main__":
    main()
