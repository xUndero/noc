# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Qtech.QSW2800.SlotRule
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

from noc.sa.profiles.Generic.get_metrics import OIDRule
from noc.core.mib import mib


class EnterpriseRule(OIDRule):
    name = "enterprise"

    def iter_oids(self, script, metric):
        if script.has_capability("SNMP | OID | EnterpriseID"):
            gen = [mib[self.expand(o, {"enterprise": script.capabilities["SNMP | OID | EnterpriseID"]})] for o in
                   self.oid]
            path = ["Usage"]
            if gen:
                yield tuple(gen), self.type, self.scale, path

