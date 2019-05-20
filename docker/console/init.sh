#!/bin/sh

CWD=$PWD
cd /shakedown
python3 setup.py develop >/init.log 2>&1
cd $CWD

/bin/bash
