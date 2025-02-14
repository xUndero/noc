# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# AlliedTelesis.AT9400.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2011 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "AlliedTelesis.AT9400.get_version"
    cache = True
    interface = IGetVersion
    rx_platform = re.compile(r"Model Name \.+ (?P<platform>AT\S+)", re.MULTILINE | re.DOTALL)
    rx_version = re.compile(
        r"^Application \.+ ATS63 v(?P<version>\S+(\s\S+)*)\s\s", re.MULTILINE | re.DOTALL
    )
    rx_serial = re.compile(r"^Serial Number \.+ (?P<serial>\S+)", re.MULTILINE | re.DOTALL)
    rx_bootprom = re.compile(
        r"^Bootloader \.+ ATS63_LOADER v(?P<bootprom>\d+\.\d+\.\d+)", re.MULTILINE | re.DOTALL
    )

    def execute(self):
        if self.has_snmp():
            try:
                pl = self.snmp.get("1.3.6.1.4.1.207.8.17.1.3.1.6.1")
                ver = self.snmp.get("1.3.6.1.4.1.207.8.17.1.3.1.5.1")
                return {"vendor": "Allied Telesis", "platform": pl, "version": ver.lstrip("v")}
            except self.snmp.TimeOutError:
                pass
        s = self.cli("show system", cached=True)
        match = self.rx_platform.search(s)
        platform = match.group("platform")
        match = self.rx_version.search(s)
        version = match.group("version")
        match = self.rx_bootprom.search(s)
        bootprom = match.group("bootprom")
        match = self.rx_serial.search(s)
        serial = match.group("serial")

        return {
            "vendor": "Allied Telesis",
            "platform": platform,
            "version": version,
            "attributes": {"Boot PROM": bootprom, "serial": serial},
        }
