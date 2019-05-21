# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event class trigger
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
        db.add_column("fm_eventclass", "trigger", models.CharField("Trigger", max_length=64, null=True, blank=True))
