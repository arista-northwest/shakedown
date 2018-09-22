# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
import pexpect

SSH_INIT_REGEX = ["(?i)are you sure you want to continue connecting",
               r'(?i)password:', pexpect.EOF, pexpect.TIMEOUT]

BACKDOOR_CREDENTIALS = ("root", "root")
