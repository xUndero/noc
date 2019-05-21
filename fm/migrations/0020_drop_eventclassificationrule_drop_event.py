# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# drop eventclassificationrule drop_event
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
        db.delete_column("fm_eventclassificationrule", "drop_event")
