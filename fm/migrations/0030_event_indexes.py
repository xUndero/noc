# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event indexes
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
        db.create_index("fm_event", ["status"])
        db.create_index("fm_event", ["timestamp"])
