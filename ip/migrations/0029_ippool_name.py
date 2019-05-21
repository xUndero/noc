# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ippool name
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db import models
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.add_column("ip_ippool", "name", models.CharField("Pool Name", max_length=64, default="default"))
