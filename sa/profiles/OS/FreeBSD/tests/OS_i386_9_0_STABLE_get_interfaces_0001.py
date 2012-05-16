# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.FreeBSD.get_interfaces test
## Auto-generated by ./noc debug-script at 16.05.2012 10:04:59
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class OS_FreeBSD_get_interfaces_Test(ScriptTestCase):
    script = "OS.FreeBSD.get_interfaces"
    vendor = "OS"
    platform = "i386"
    version = "9.0-STABLE"
    input = {}
    result = [{'forwarding_instance': 'default',
  'interfaces': [{'admin_status': True,
                  'descriptions': 'Uplink',
                  'mac': '00:E0:81:40:8D:56',
                  'name': 'em0',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'descriptions': 'Uplink',
                                     'ipv4_addresses': ['10.111.0.14/24',
                                                        '192.168.1.1/24'],
                                     'is_ipv4': True,
                                     'mac': '00:E0:81:40:8D:56',
                                     'name': 'em0',
                                     'oper_status': True},
                                    {'admin_status': True,
                                     'ipv4_addresses': ['10.116.0.211/16'],
                                     'is_ipv4': True,
                                     'mac': '00:E0:81:40:8D:56',
                                     'name': 'em0.256',
                                     'oper_status': True,
                                     'vlan_ids': [256]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:E0:81:40:8D:57',
                  'name': 'em1',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv6_addresses': ['2001:db8:bdbd::123/48'],
                                     'is_ipv6': True,
                                     'mac': '00:E0:81:40:8D:57',
                                     'name': 'em1',
                                     'oper_status': False}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'name': 'lo0',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_addresses': ['127.0.0.1/8'],
                                     'ipv6_addresses': ['::1/128'],
                                     'is_ipv4': True,
                                     'is_ipv6': True,
                                     'name': 'lo0',
                                     'oper_status': False}],
                  'type': 'loopback'},
                 {'admin_status': True,
                  'mac': '00:1F:C6:72:FD:8A',
                  'name': 'ae0',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_addresses': ['10.111.0.151/24'],
                                     'is_ipv4': True,
                                     'mac': '00:1F:C6:72:FD:8A',
                                     'name': 'ae0',
                                     'oper_status': True}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:15:AF:9F:F9:A4',
                  'name': 'ath0',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'mac': '00:15:AF:9F:F9:A4',
                                     'name': 'ath0',
                                     'oper_status': True},
                                    {'admin_status': True,
                                     'mac': '00:15:AF:9F:F9:A4',
                                     'name': 'wlan0',
                                     'oper_status': False}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'name': 'lo0',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_addresses': ['127.0.0.1/8'],
                                     'is_ipv4': True,
                                     'name': 'lo0',
                                     'oper_status': False}],
                  'type': 'loopback'}],
  'type': 'ip'}]
    motd = ''
    cli = {
## 'ifconfig -v'
'ifconfig -v': """ ifconfig -v
ae0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
\toptions=82018<VLAN_MTU,VLAN_HWTAGGING,WOL_MAGIC,LINKSTATE>
\tether 00:1f:c6:72:fd:8a
\tinet 10.111.0.151 netmask 0xffffff00 broadcast 10.111.0.255
\tmedia: Ethernet autoselect (100baseTX <full-duplex>)
\tstatus: active
ath0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 2290
\tether 00:15:af:9f:f9:a4
\tmedia: IEEE 802.11 Wireless Ethernet autoselect mode 11g
\tstatus: associated
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
\toptions=3<RXCSUM,TXCSUM>
\tinet 127.0.0.1 netmask 0xff000000 
\tgroups: lo 
wlan0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
\tether 00:15:af:9f:f9:a4
\tmedia: IEEE 802.11 Wireless Ethernet autoselect (autoselect)
\tstatus: no carrier
\tssid Noob channel 8 (2447 MHz 11g) bssid 00:00:00:00:00:00
\tregdomain 96 country DEBUG indoor ecm authmode OPEN -wps -tsn
\tprivacy OFF deftxkey UNDEF powersavemode OFF powersavesleep 100
\ttxpower 20 txpowmax 50.0 -dotd rtsthreshold 2346 fragthreshold 2346
\tbmiss 7
\t11a     ucast NONE    mgmt  6 Mb/s mcast  6 Mb/s maxretry 6
\t11b     ucast NONE    mgmt  1 Mb/s mcast  1 Mb/s maxretry 6
\t11g     ucast NONE    mgmt  1 Mb/s mcast  1 Mb/s maxretry 6
\tturboA  ucast NONE    mgmt  6 Mb/s mcast  6 Mb/s maxretry 6
\tturboG  ucast NONE    mgmt  1 Mb/s mcast  1 Mb/s maxretry 6
\tsturbo  ucast NONE    mgmt  6 Mb/s mcast  6 Mb/s maxretry 6
\t11na    ucast NONE    mgmt 12 MCS  mcast 12 MCS  maxretry 6
\t11ng    ucast NONE    mgmt  2 MCS  mcast  2 MCS  maxretry 6
\thalf    ucast NONE    mgmt  3 Mb/s mcast  3 Mb/s maxretry 6
\tquarter ucast NONE    mgmt  1 Mb/s mcast  1 Mb/s maxretry 6
\tscanvalid 60 bgscan bgscanintvl 300 bgscanidle 250
\troam:11a     rssi    7dBm rate 12 Mb/s
\troam:11b     rssi    7dBm rate  1 Mb/s
\troam:11g     rssi    7dBm rate  5 Mb/s
\troam:turboA  rssi    7dBm rate 12 Mb/s
\troam:turboG  rssi    7dBm rate 12 Mb/s
\troam:sturbo  rssi    7dBm rate 12 Mb/s
\troam:11na    rssi    7dBm  MCS  1    
\troam:11ng    rssi    7dBm  MCS  1    
\troam:half    rssi    7dBm rate  6 Mb/s
\troam:quarter rssi    7dBm rate  3 Mb/s
\t-pureg protmode CTS -ht -htcompat -ampdu ampdulimit 8k ampdudensity 8
\t-amsdu -shortgi htprotmode RTSCTS -puren smps -rifs wme burst -dwds
\troaming AUTO bintval 0
\tAC_BE cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm ack
\t      cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm
\tAC_BK cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm ack
\t      cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm
\tAC_VI cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm ack
\t      cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm
\tAC_VO cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm ack
\t      cwmin  0 cwmax  0 aifs  0 txopLimit   0 -acm
\tgroups: wlan """, 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
