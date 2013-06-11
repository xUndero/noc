# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## pm.check application
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.app import ExtDocApplication, view
from noc.pm.models.check import PMCheck
from noc.pm.pmprobe.checks.base import check_registry


class PMCheckApplication(ExtDocApplication):
    """
    PMCheck application
    """
    title = "Checks"
    menu = "Checks"
    model = PMCheck
    query_fields = ["name"]

    def get_launch_info(self, request):
        li = super(PMCheckApplication, self).get_launch_info(request)
        li["params"]["check_forms"] = dict(
            (check_registry[c].name, check_registry[c].form)
            for c in check_registry
            if check_registry[c].form)
        return li
