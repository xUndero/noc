# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# zonerecordtype is visible
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
        db.add_column("dns_dnszonerecordtype", "is_visible", models.BooleanField("Is Visible?", default=True))
