# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# notify
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
            "cm_objectcategory", "notify_immediately", models.TextField("Notify Immediately", blank=True, null=True)
        )
        db.add_column("cm_objectcategory", "notify_delayed", models.TextField("Notify Delayed", blank=True, null=True))
