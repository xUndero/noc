# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# AlliedTelesis.AT8000S.get_vlans
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# coded by azhur
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetvlans import IGetVlans
import re


class Script(BaseScript):
    name = "AlliedTelesis.AT8000S.get_vlans"
    interface = IGetVlans
    rx_vlan_line = re.compile(r"^(?P<vlan_id>\d{1,4})\s+(?P<name>\S+)\s")

    """
    Need fix for cmp(x["vlan_id"], y["vlan_id"])

    def execute_snmp(self):
        oids = {}
        # Get OID -> VLAN ID mapping
        for oid, v in self.snmp.getnext("1.3.6.1.2.1.17.7.1.4.2.1.3"):  # dot1qVlanFdbId
            oids[oid.split(".")[-1]] = v
        # Get VLAN names
        result = [{"vlan_id": 1, "name": "1"}]
        for oid, v in self.snmp.getnext("1.3.6.1.2.1.17.7.1.4.3.1.1"):  # dot1qVlanStaticName
            o = oid.split(".")[-1]
            result += [{"vlan_id": int(oids[o]), "name": v.strip()}]
        return sorted(result, lambda x, y: cmp(x["vlan_id"], y["vlan_id"]))
    """

    def execute_cli(self):
        vlans = self.cli("show vlan")
        r = []
        for l in vlans.split("\n"):
            match = self.rx_vlan_line.match(l.strip())
            if match:
                r += [{"vlan_id": match.group("vlan_id"), "name": match.group("name")}]
        return r
