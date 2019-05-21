# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnszone serial
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
        db.execute("ALTER TABLE dns_dnszone ALTER serial DROP DEFAULT")
        db.execute("ALTER TABLE dns_dnszone ALTER serial TYPE INTEGER USING serial::integer")
        db.execute("ALTER TABLE dns_dnszone ALTER serial SET DEFAULT 0")
        db.execute("ALTER TABLE dns_dnszone ALTER serial SET NOT NULL")
