# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# no object group
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    depends_on = (("cm", "0016_no_objectgroup"),)

    def migrate(self):
        for t in ["sa_managedobject_groups", "sa_managedobjectselector_filter_groups", "sa_objectgroup"]:
            self.db.drop_table(t)
