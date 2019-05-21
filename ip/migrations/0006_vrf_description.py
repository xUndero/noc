# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# vrf description
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.add_column(
            "ip_vrfgroup", "description", models.CharField("Description", blank=True, null=True, max_length=128)
        )
        db.add_column("ip_vrf", "description", models.CharField("Description", blank=True, null=True, max_length=128))
