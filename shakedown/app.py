#!/usr/bin/env python3.5

import flask
import json
import sh
import os
#from flask import Flask
app = flask.Flask(__name__)

HOME = os.path.expanduser("~")
SHAKEDOWN_DIR = os.path.join(HOME, ".shakedown")
#os.environ['GIT_DIR'] = SHAKEDOWN_DIR


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<string:testrun>/<string:testcase>", methods=["GET", "POST"])
def do_testcase(testrun, testcase):
    content = json.dumps({
        "testrun": testrun,
        "testcase": testcase
    })
    resp = flask.Response(content)
    resp.headers['Content-Type:'] = 'application/json'
    return resp

if __name__ == "__main__":

    sh.mkdir("-p", SHAKEDOWN_DIR    )
    # #sh.cd(SHAKEDOWN_PATH)
    # sh.git("init")
    # sh.git("add", ".")

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
