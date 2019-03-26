# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Axis
# OS:     VAPIX
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Axis.VAPIX"

    def get_list(self, script):
        v = script.http.get(
            "/axis-cgi/admin/param.cgi?action=list",
            eof_mark="root.Time.NTP", cached=True, use_basic=True
        )
        return v

    def get_dict(self, script):
        r = {}
        v = self.get_list(script)
        for line in v.splitlines():
            key, value = line.split("=", 1)
            r[key] = value
        return r
