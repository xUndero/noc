# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobject set segment
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration
from noc.lib.nosql import get_db


class Migration(BaseMigration):
    def migrate(self):
        # Get first segment
        ns = get_db().noc.networksegments.find_one({}, sort=[("name", 1)])
        self.db.execute("""
            UPDATE sa_managedobject
            SET segment=%s
            """, [str(ns["_id"])])
