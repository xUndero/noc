# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# inv.platform application
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.lib.app import ExtDocApplication, view
from noc.inv.models.platform import Platform
from noc.core.translation import ugettext as _


class PlatformApplication(ExtDocApplication):
    """
    Platform application
    """
    title = "Platform"
    menu = [_("Setup"), _("Platforms")]
    model = Platform
    query_fields = [
        "name__icontains", "description__icontains"
    ]
