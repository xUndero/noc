# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Nateks.FlexGainACE16.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory


class Script(BaseScript):
    name = "Nateks.FlexGainACE16.get_inventory"
    interface = IGetInventory

    def execute(self):
        v = self.scripts.get_version()
        return [
            {
                "type": "CHASSIS",
                "vendor": "Nateks",
                "part_no": [v["platform"]],
                "serial": v["attributes"]["Serial Number"],
            }
        ]
