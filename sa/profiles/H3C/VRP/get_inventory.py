# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# H3C.VRP.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory


class Script(BaseScript):
    name = "H3C.VRP.get_inventory"
    interface = IGetInventory

    def execute(self):
        v = self.scripts.get_version()
        return [
            {
                "type": "CHASSIS",
                "vendor": "H3C",
                "part_no": [v["platform"]],
                "serial": v["attributes"]["Serial Number"],
            }
        ]
