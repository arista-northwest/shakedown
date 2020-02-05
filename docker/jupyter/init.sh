#!/bin/bash

# CWD=$PWD
# cd /shakedown
# python3 setup.py develop
# cd $CWD

jupyter notebook --NotebookApp.token='' --allow-root --port=8888 --no-browser --ip=0.0.0.0
