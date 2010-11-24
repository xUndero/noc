# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Force10.FTOS.get_arp test
## Auto-generated by manage.py debug-script at 2010-11-24 22:57:28
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Force10_FTOS_get_arp_Test(ScriptTestCase):
    script="Force10.FTOS.get_arp"
    vendor="Force10"
    platform='C300'
    version='8.3.1.1'
    input={}
    result=[{'interface': 'Po 1', 'ip': '10.33.32.1', 'mac': '00:01:E8:6D:1F:1C'},
 {'interface': 'Po 1', 'ip': '10.33.32.7', 'mac': '00:24:81:D9:2D:41'},
 {'interface': 'Po 1', 'ip': '10.33.32.9', 'mac': '00:23:EA:D6:2E:41'},
 {'interface': 'Po 1', 'ip': '10.33.32.11', 'mac': '00:23:AC:83:F3:C1'},
 {'interface': 'Po 1', 'ip': '10.33.32.54', 'mac': '00:01:E8:81:E1:FA'}]
    motd=' \n'
    cli={
## 'show arp'
'show arp': """show arp

Protocol    Address         Age(min)  Hardware Address    Interface  VLAN             CPU
-----------------------------------------------------------------------------------------
Internet    10.33.32.1            0   00:01:e8:6d:1f:1c   Po 1       Vl 2             CP
Internet    10.33.32.2            -   00:01:e8:79:36:4e      -       Vl 2             CP
Internet    10.33.32.7           96   00:24:81:d9:2d:41   Po 1       Vl 2             CP
Internet    10.33.32.9           13   00:23:ea:d6:2e:41   Po 1       Vl 2             CP
Internet    10.33.32.11          75   00:23:ac:83:f3:c1   Po 1       Vl 2             CP
Internet    10.33.32.54          76   00:01:e8:81:e1:fa   Po 1       Vl 2             CP""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
