# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_udld_neighbors
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import re
## NOC modules
from noc.sa.script import NOCScript
from noc.sa.interfaces import IGetUDLDNeighbors


class Script(NOCScript):
    name = "Cisco.IOS.get_udld_neighbors"
    implements = [IGetUDLDNeighbors]

    rx_split = re.compile(r"^Interface\s+", re.MULTILINE | re.IGNORECASE)
    rx_entry = re.compile(
        r"^\s+Current neighbor state: (?P<state>Bidirectional)\n"
        r"^\s+Device ID: (?P<remote_device>\S+)\n"
        r"^\s+Port ID: (?P<remote interface>\S+)\n"
        r"^\s+Neighbor echo \d+ device: (?P<local_device>\S+)\n",
        re.MULTILINE | re.IGNORECASE
    )

    def execute(self):
        r = []
        s = self.cli("show udld")
        for p in self.rx_split.split(s):
            r = p.split("\n", 1)
            if len(r) != 2 or not r[1].startswith("---"):
                continue
            local_interface = r[0].split()
            match = self.rx_entry.match(r[1])
            if not match:
                return
            r += [{
                  "local_device": match.group("local_debvice"),
                  "local_interface": local_interface,
                  "remote_device": match.group("remote_device"),
                  "remote_interface": match.group("remote_interface"),
                  "state": match.group("state").upper()
            }]
        return r
