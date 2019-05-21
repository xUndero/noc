# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Set VRF.rd to nullable/non-unique
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
        db.execute("ALTER TABLE ip_vrf DROP CONSTRAINT \"ip_vrf_rd_key\"")
        db.execute("ALTER TABLE ip_vrf ALTER COLUMN rd DROP NOT NULL")
