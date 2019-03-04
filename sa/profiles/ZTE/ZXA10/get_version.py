# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ZTE.ZXA10.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re
# re modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "ZTE.ZXA10.get_version"
    cache = True
    interface = IGetVersion

    rx_platform = re.compile(
        r"^\d+\s+(?P<platform>\S+)MBRack\s+.+\n", re.MULTILINE
    )
    rx_version = re.compile(
        r"Serial Number\s+:\s+(?P<serial>\S+)\s+.+\n"
        r"CPLD Version.+\n"
        r"Boot Version\s+:\s+(?P<bootprom>\S+)\s+.+\n"
        r"Software Version\s+:\s+(?P<version>\S+)\s+.+\n",
        re.MULTILINE
    )

    def execute_cli(self):
        v = self.cli("show rack")
        match = self.rx_platform.search(v)
        platform = match.group("platform")
        v = self.cli("show card type MCCARD")
        match = self.rx_version.search(v)
        return {
            "vendor": "ZTE",
            "platform": platform,
            "version": match.group("version"),
            "attributes": {
                "Boot PROM": match.group("bootprom"),
                "Serial Number": match.group("serial")
            }
        }
