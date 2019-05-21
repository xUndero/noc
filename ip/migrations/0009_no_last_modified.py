# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# no last modified
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
        db.delete_column("ip_ipv4block", "modified_by_id")
        db.delete_column("ip_ipv4block", "last_modified")
        db.delete_column("ip_ipv4address", "modified_by_id")
        db.delete_column("ip_ipv4address", "last_modified")
