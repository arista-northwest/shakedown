Arista IPython Magics
=====================


Booting the Vagrant Image
-------------------------

```bash
$ git clone https://github.com/arista-northwest/shakedown.git
$ cd shakedown
$ vagrant up

```

Browse to: http://localhost:8008
(username: ubuntu, password: ubuntu)

### Example Usage

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


```
%%sdsend tor spine
show version
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
