# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# no category
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
        db.delete_table("kb_kbentrytemplate_categories")
        db.delete_table("kb_kbentry_categories")
        db.delete_table("kb_kbcategory")
