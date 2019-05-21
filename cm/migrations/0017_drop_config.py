# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# drop config
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    depends_on = [("sa", "0077_drop_repo_path")]

    def migrate(self):
        db.drop_table("cm_config")
