# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Drop django-tagging tables
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        for t in ["tagging_taggeditem", "tagging_tag"]:
            if db.execute("SELECT COUNT(*) FROM pg_class WHERE relname='%s'" % t)[0][0] == 1:
                db.drop_table(t)
