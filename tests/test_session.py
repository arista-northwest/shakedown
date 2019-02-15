import os
import re
import pytest
from shakedown.session import sessions
from shakedown.config import config
import eapi
from pprint import pprint


path = os.path.dirname(os.path.realpath(__file__))

CONFIG = os.environ.get("SHAKEDOWN_CONFIG", os.path.join(path, "../examples/shakedown.yml"))

config.load(CONFIG)

def test_session():
    response = sessions.send("dut", ["show version"])

    pprint(response)

def test_bogus():
    with pytest.raises(eapi.EapiResponseError):
        response = sessions.send("dut", ["show bogus"])

def test_callback():

    def _cb(response):
        pass

    response = sessions.send("dut", ["show version"], callback=_cb)

def test_until():

    def _cb(response):
        pass

    response = sessions.send("dut", ["show clock"], until=r"\:?5")


def test_filter():
    filt = r"s?dut"
    filtered = sessions.filter(filt)
    r = re.compile(filt)
    for sess in filtered:
        v = filter(r.search, [sess.endpoint] + sess.tags)
        assert list(v), "filtered items do not match the filter"
