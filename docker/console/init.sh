#!/bin/sh

CWD=$PWD
cd /shakedown
python3 setup.py develop
cd $CWD

/bin/bash
