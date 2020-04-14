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
    dependency_links=[
        'git+https://github.com/arista-northwest/eapi-py.git#egg=eapi-py'
    ],
    install_requires=[
        "pytest==5.4.1",
        "PyYAML==5.3.1",
        "pexpect==4.8.0",
        "Jinja2==2.11.2",
        "sh==1.12.14",
        "mistune==0.8.4",
        "tinydb==3.15.2",
        "tinymongo==0.2.0",
        "pandas==1.0.3",
        "matplotlib==3.2.1",
        "numpy==1.18.2",
        "eapi-py"
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
