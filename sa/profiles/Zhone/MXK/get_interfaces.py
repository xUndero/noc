# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Zhone.MXK.get_interfaces
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_interfaces import Script as BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.mac import MAC


class Script(BaseScript):
    name = "Zhone.MXK.get_interfaces"
    interface = IGetInterfaces

    rx_ifbase = re.compile(r"^(\d+-\S+-\d+-\d+)/\S+$", re.MULTILINE)
    rx_ifbase1 = re.compile(r"^(\d+/\S+/\d+/\d+)/\S+$", re.MULTILINE)
    rx_mac = re.compile(
        r"^\s*MAC Address are enabled for (?P<count>\d+) address\(es\) starting at:\s*\n"
        r"^\s*(?P<mac>\S+)",
        re.MULTILINE,
    )
    rx_ether = re.compile(r"^ether\s+(?P<name>1-a-\d+-0/eth)\s*\n", re.MULTILINE)
    rx_ether_count = re.compile(r"^(?P<count>\d+) entries found.", re.MULTILINE)
    rx_ether_status = re.compile(
        r"^\s*Line Type-+> ETHERNET \(7\)\s*\n"
        r"^\s*GroupId -+> \d+\s*\n"
        r"^\s*Status -+> (?P<status>.+?)\s*\n"
        r"^\s*Redundancy .+\n"
        r"^\s*TxClk .+\n"
        r"^\s*RefClkSrc .+\n"
        r"^\s*If_index -+> (?P<snmp_ifindex>\d+)\s*\n"
        r"^\s*Physical -+> (?P<ifname>\S+)\s*\n",
        re.MULTILINE,
    )
    rx_ip = re.compile(
        r"^(?P<name>\S+)\s+UP\s+(?P<rd>\d+)\s+(?P<ip>\d+\S+)\s+(?P<mac>\S+)\s+(?P<alias>\S+)\s*\n",
        re.MULTILINE,
    )

    def execute_cli(self):
        interfaces = []
        mac = ""
        v = self.cli("eeshow card a")
        match = self.rx_mac.search(v)
        start_mac = match.group("mac")
        count_mac = match.group("count")
        v = self.cli("list ether")
        match = self.rx_ether_count.search(v)
        if int(count_mac) != int(match.group("count")):
            raise self.CLIOperationError()
        ifcount = 0
        for match in self.rx_ether.finditer(v):
            ifname = self.rx_ifbase.search(match.group("name")).group(1)
            mac = MAC(int(MAC(start_mac)) + ifcount)
            ifcount = ifcount + 1
            c = self.cli("showlinestatus 1 a %s" % str(ifcount))
            match1 = self.rx_ether_status.search(c)
            admin_status = match1.group("status") != "ADMIN DOWN (3)"
            oper_status = match1.group("status") == "ACTIVE (1)"
            iface = {
                "name": ifname,
                "type": "physical",
                "admin_status": admin_status,
                "oper_status": oper_status,
                "mac": mac,
                "snmp_ifindex": match1.group("snmp_ifindex"),
                "subinterfaces": [
                    {
                        "name": match.group("name"),
                        "admin_status": admin_status,
                        "oper_status": oper_status,
                        "enabled_afi": ["BRIDGE"],
                        "mac": mac,
                        "snmp_ifindex": match1.group("snmp_ifindex"),
                    }
                ],
            }
            interfaces += [iface]
        v = self.cli("interface show")
        for match in self.rx_ip.finditer(v):
            ifname = self.rx_ifbase1.search(match.group("name")).group(1)
            ifname = ifname.replace("/", "-")
            for i in interfaces:
                if i["name"] == ifname:
                    i["subinterfaces"] += [
                        {
                            "name": match.group("name"),
                            "oper_status": True,
                            "admin_status": True,
                            "description": match.group("alias"),
                            "mac": match.group("mac"),
                            "enable_afi": ["IPv4"],
                            "ip_addresess": [match.group("ip")],
                        }
                    ]
                    break

        return [{"interfaces": interfaces}]
