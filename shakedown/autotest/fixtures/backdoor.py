


import pytest
from shakedown.backdoor import Session

@pytest.fixture(scope="module")
def backdoor(dut, request):
    bkd = Session()
    request.addfinalizer(lambda: bkd.close())

    bkd.open(dut.host)

    return bkd
