


import pytest
from shakedown.backdoor import Backdoor

@pytest.fixture(scope="module")
def backdoor(dut, request):
    bkd = Backdoor()
    request.addfinalizer(lambda: bkd.close())

    bkd.open(dut.host)

    return bkd
