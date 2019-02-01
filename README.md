Shakedown - Acceptance testing automation
=========================================

## Installation

```bash
$ git clone https://github.com/arista-northwest/shakedown.git
$ cd shakedown
```

Bring up docker containers (jupyter and jenkins) (w/ docker-compose)

```bash
cd docker
docker-compose up jupyter
```
Then open a browser to http://localhost:8888

```bash
cd docker
docker-compose up jenkins
```
Then open a browser to http://localhost:8080

or install just the toolset directly

```bash
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

## Demo lab setup

```
hosts:

192.168.56.11 veos-1
192.168.56.12 veos-2

+--------+             +--------+
|        |             |        |
| VEOS-1 | <=========> | VEOS-2 |
|        |             |        |
+--------+             +--------+
```

## Command line example

Basic test run using included example:

```bash
$ cd examples
$ sdtest -vs --config config.yml tests/test_001_basics.py
```

Or in Docker:

```bash
$ docker-compose exec jenkins /bin/bash
jenkins@2001deadbeef:/$ cd /testplan/
jenkins@2001deadbeef:/testplan$ sdtest -vs --config config.yml tests/test_001_basics.py
```

Example test module

```python
# -*- coding: utf-8 -*-

"""
title: Defaults Collection

description: |
    Make sure the DUT is on the correct software version

"""
import re
import pytest
import arcomm

def test_version(sessions, sdconfig, testconfig):
    """Autotest will scan the class for any methods that start with 'test'."""

    version = testconfig["software_version"]
    response = sessions.send(r"dut", "show version")

    for r in response:
        assert version in str(r[0].output), \
            "Software version should be {}".format(version)

def test_bogus(sessions, sdconfig, testconfig):
    """Run a bogus command. should throw error"""
    with pytest.raises(arcomm.ExecuteFailed):
        response = sessions.send(r"dut", "show bogus")
```

## IPython + Jupyter Notebooks

After booting the vagrant image. Browse to: http://localhost:8008

(username: _ubuntu_, password: _ubuntu_)

### Example Usage


Load a configuration file (setting can be overridden in-line)

```
%%sdconfig [config-file]
vars:
    vrf: management
    upgrade: "flash:EOS-4.19.1F.swi"
    downgrade: "flash:EOS-4.18.3.1F.swi"

connections:
  veos-1:
    creds: [ admin, "" ]
    protocol: eapi+http
    tags: [ dut, tor ]

  veos-2:
    creds: [ admin,  "" ]
    tags: [ sdut, spine ]

tests:
    downgrade:
        testrail_case_id: C12345
```

example cell:

```
%%sdsend tor spine
show version
```

outputs:

```
    host: 7280cr-01
    status: ok
    commands:
      - command: show version
        output: |
          Arista DCS-7280CR-48-F
          Hardware version:    01.00
          Serial number:       JPE16123175
          System MAC address:  444c.a896.ca19

          Software image version: 4.16.6FX-7500R
          Architecture:           i386
          Internal build version: 4.16.6FX-7500R-3217494.4166FX7500R
          Internal build ID:      7b5b44e2-3f61-44d8-b386-67dabb3b2ed0

          Uptime:                 26 minutes
          Total memory:           16035752 kB
          Free memory:            11410748 kB

    host: 7280cr-02
    status: ok
    commands:
      - command: show version
        output: |
          Arista DCS-7280CR-48-F
          Hardware version:    01.00
          Serial number:       JPE16151910
          System MAC address:  444c.a896.e9e1

          Software image version: 4.16.6FX-7500R
          Architecture:           i386
          Internal build version: 4.16.6FX-7500R-3217494.4166FX7500R
          Internal build ID:      7b5b44e2-3f61-44d8-b386-67dabb3b2ed0

          Uptime:                 2 weeks, 3 days, 4 hours and 17 minutes
          Total memory:           16035752 kB
          Free memory:            11219016 kB
```
