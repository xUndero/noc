# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# drop groups and fields
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
        # Drop groups and fields
        db.drop_column("cm_objectnotify", "group_id")
