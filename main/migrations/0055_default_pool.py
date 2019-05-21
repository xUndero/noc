# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Create *default* pool
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.lib.nosql import get_db
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    depends_on = [("sa", "0005_activator")]

    def migrate(self):
        mdb = get_db()
        for a_id, name in db.execute("SELECT id, name FROM sa_activator"):
            mdb.noc.pools.insert_one({"name": "P%04d" % a_id, "description": name})

    def backwards(self):
        pass
