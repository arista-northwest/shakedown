# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import io
import os
import re
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 5, 0):
    raise NotImplementedError("Sorry, you need at least Python 3.5 to install.")

with io.open('shakedown/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \"(.*?)\"', f.read()).group(1)

with open(os.path.join('README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "shakedown",
    version = version,
    author = "Jesse Mather",
    author_email = "jmather@arista.com",
    description = "",
    long_description = long_description,
    # dependency_links=[
    #     'git+https://github.com/arista-northwest/eapi-py.git#egg=eapi-py'
    # ],
    install_requires=[
        "pytest",
        "PyYAML",
        "pexpect",
        "Jinja2",
        "sh",
        "mistune",
        "tinydb",
        "tinymongo",
        "pandas",
        "matplotlib",
        "numpy",
        "eapi-py==0.4.1"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Terminals"
    ],
    packages = find_packages(),
    package_data={'': ['settings.yml']},
    url = "https://github.com/arista-northwest1/shakedown",
    license = "MIT Licesnse",
    entry_points = {
        'console_scripts': [
            'sdtest = shakedown.autotest.entry:main',
        ]
    }
)
