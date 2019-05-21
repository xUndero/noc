# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# rename rr type is_visible
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.rename_column("dns_dnszonerecordtype", "is_visible", "is_active")
