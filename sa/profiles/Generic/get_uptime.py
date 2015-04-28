# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Generic.get_snmp_get
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.sa.script import Script as NOCScript
from noc.sa.interfaces.igetuptime import IGetUptime
from noc.lib.mib import mib


class Script(NOCScript):
    """
    Returns system uptime in the thousands of second
    """
    name = "Generic.get_uptime"
    implements = [IGetUptime]
    requires = []

    def execute(self):
        if self.snmp and self.access_profile.snmp_ro:
            try:
                return self.snmp.get(mib["SNMPv2-MIB::sysUpTime", 0])
            except self.snmp.TimeOutError:
                pass
        return None
