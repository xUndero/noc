# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnsserver sync_channel
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
            "dns_dnsserver", "sync_channel", models.CharField("Sync channel", max_length=64, blank=True, null=True)
        )
