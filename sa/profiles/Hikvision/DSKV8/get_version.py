# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Hikvision.DSKV8.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
import xml.etree.ElementTree as ElementTree
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Hikvision.DSKV8.get_version"
    interface = IGetVersion
    cache = True

    rx_date = re.compile(r"(?P<yy>\d\d)(?P<mm>\d\d)(?P<dd>\d\d)")

    def execute(self):
        ns = {'isapi': 'http://www.isapi.org/ver20/XMLSchema'}
        v = self.http.get("/ISAPI/System/deviceInfo", use_basic=True)
        root = ElementTree.fromstring(v)

        return {
            "vendor": 'Hikvision',
            "platform": root.find("isapi:model", ns).text,
            "version": root.find("isapi:firmwareVersion", ns).text,
            "attributes": {
                # "Boot PROM": match.group("bootprom"),
                "Build Date": root.find("isapi:firmwareReleasedDate", ns).text,
                "HW version": root.find("isapi:firmwareVersion", ns).text,
                "Serial Number": root.find("isapi:serialNumber", ns).text
                # "Firmware Type":
            }
        }
