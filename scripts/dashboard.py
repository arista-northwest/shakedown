#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import argparse
import json

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(prog="arcomm")
    arg = parser.add_argument

    arg("reports_dir", nargs="*")
    # arg("-v", "--version", action="store_true", help="display version info")

    # arg("--protocol", help=("set the protocol. By default 'eapi' is used."),
    #     choices=["eapi", "eapi+https", "mock", "ssh"])

if __name__ == "__main__":
    pass