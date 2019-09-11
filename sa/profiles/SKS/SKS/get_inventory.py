# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# SKS.SKS.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory
from noc.lib.text import parse_table


class Script(BaseScript):
    name = "SKS.SKS.get_inventory"
    interface = IGetInventory
    cache = True

    rx_e1_part_no = re.compile(r"^sysType\s+(?P<part_no>.+?)\s*\n", re.MULTILINE)
    rx_e1_serial = re.compile(r"^serialNum\s+(?P<serial>\S+)\s*\n", re.MULTILINE)
    rx_e1_revision = re.compile(r"^hwVer\s+(?P<revision>\S+)\s*\n", re.MULTILINE)
    rx_port = re.compile(
        r"^(?P<port>(?:Fa|Gi|Te|Po)\S+)\s+(?P<type>\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(?:Up|Down|Not Present)",
        re.MULTILINE | re.IGNORECASE,
    )
    rx_sfp_vendor = re.compile("SFP vendor name:(?P<vendor>\S+)")
    rx_sfp_serial = re.compile("SFP serial number:(?P<serial>\S+)")

    def execute(self):
        v = self.cli("show version", cached=True)
        if "Unit" in v:
            stack = {}
            r = []
            t = parse_table(v)
            for i in t:
                stack[i[0]] = {"type": "CHASSIS", "vendor": "SKS", "revision": i[3]}
            v = self.cli("show system", cached=True)
            t = parse_table(v, footer=r"Unit\s+Temperature")
            for i in t:
                platform = i[1]
                if platform == "SKS 10G":
                    platform = "SKS-16E1-IP-1U"
                elif platform.startswith("SKS"):
                    platform = "SW-24"
                if not i[0]:
                    break
                stack[i[0]]["part_no"] = platform
            v = self.cli("show system id", cached=True)
            t = parse_table(v)
            for i in t:
                stack[i[0]]["serial"] = i[1]
            for i in stack:
                r += [stack[i]]
            return r
        else:
            v = self.scripts.get_version()
            r = [
                {
                    "type": "CHASSIS",
                    "vendor": "SKS",
                    "part_no": v["platform"],
                    "revision": v["attributes"]["HW version"],
                }
            ]
            if "Serial Number" in v["attributes"]:
                r[0]["serial"] = v["attributes"]["Serial Number"]

            v = self.cli("?", command_submit="")
            if "enter E1 context" in v:
                with self.profile.e1(self):
                    v = self.cli("info")
                    part_no = self.rx_e1_part_no.search(v).group("part_no")
                    serial = self.rx_e1_serial.search(v).group("serial")
                    revision = self.rx_e1_revision.search(v).group("revision")
                    r += [
                        {
                            "type": "MODULE",
                            "vendor": "SKS",
                            "part_no": part_no,
                            "serial": serial,
                            "revision": revision,
                        }
                    ]

            v = self.cli("show interfaces status", cached=True)
            for match in self.rx_port.finditer(v):
                if match.group("type") in ["1G-Combo-C", "1G-Combo-F", "10G-Combo-C", "10G-Combo-F"]:
                    c = self.cli(
                        "show fiber-ports optical-transceiver interface %s" % match.group("port")
                    )
                    match1 = self.rx_sfp_serial.search(c)
                    if match1:
                        r += [
                            {
                                "type": "XCVR",
                                "vendor": "NONAME",
                                "part_no": "Unknown | Transceiver | SFP",
                                "number": match.group("port")[-1:],
                                "serial": match1.group("serial"),
                            }
                        ]
        return r
