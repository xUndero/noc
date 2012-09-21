# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_version test
## Auto-generated by ./noc debug-script at 21.09.2012 16:17:46
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class EdgeCore_ES_get_version_Test(ScriptTestCase):
    script = "EdgeCore.ES.get_version"
    vendor = "EdgeCore"
    platform = "ES3510"
    version = "1.1.0.26"
    input = {}
    result = {'attributes': {'HW version': 'R01', 'Serial Number': '0012CF8B00D0'},
 'platform': 'ES3510',
 'vendor': 'EdgeCore',
 'version': '1.1.0.26'}
    motd = ''
    cli = {
## 'show version'
'show version': """show version
 Serial Number:           0012CF8B00D0
 Service Tag:             
 Hardware Version:        R01
 EPLD Version:            0.00
 Number of Ports:         10
 Main Power Status:       Up
 Loader Version:          1.0.0.2
 Boot ROM Version:        1.0.0.5
 Operation Code Version:  1.1.0.26""", 
## 'show system'
'show system': """show system
System Description: Layer2+ Fast Ethernet Standalone Switch ES3510
System OID String: 1.3.6.1.4.1.259.8.1.6
System Information
 System Up Time:          19 days, 13 hours, 18 minutes, and 46.10 seconds
 System Name:             Maliy_pr_Petr_Stor_2/5_Mika
 System Location:         [NONE]
 System Contact:          [NONE]
 MAC Address (Unit1):     00-12-CF-8B-00-D0
 Web Server:              Enabled
 Web Server Port:         80
 Web Secure Server:       Enabled
 Web Secure Server Port:  443
 Telnet Server:           Enable
 Telnet Server Port:      23
 Authentication Login:     TACACS Local None
 Jumbo Frame:             Disabled 

 POST Result:              
DUMMY Test 1 ................. PASS
UART Loopback Test ........... PASS
DRAM Test .................... PASS
Switch Int Loopback Test ..... PASS

Done All Pass.""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
