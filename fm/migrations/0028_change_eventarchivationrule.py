# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# change eventarchivationrule
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
        db.create_unique('fm_eventarchivationrule', ['event_class_id', 'action'])
        try:
            db.delete_unique('fm_eventarchivationrule', ['event_class_id'])
        except Exception:
            pass
