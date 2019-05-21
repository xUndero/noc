# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# object notify drop emails
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
        db.drop_column("cm_objectnotify", "emails")
        db.execute("ALTER TABLE cm_objectnotify ALTER COLUMN notification_group_id SET NOT NULL")
