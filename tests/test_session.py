import pytest
from shakedown.session import sessions
from shakedown.config import config
import eapi
from pprint import pprint

CONFIG_FILE="../examples/shakedown.yml"

config.load(CONFIG_FILE)

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

    response = sessions.send("dut", ["show clock"], until="\:?5")
