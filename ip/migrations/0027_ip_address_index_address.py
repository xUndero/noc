# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ip_address index address
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
        db.create_index("ip_address", ["address"], db_tablespace="")
