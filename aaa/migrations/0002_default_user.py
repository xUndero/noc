# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Create default user
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os

# Third-party modules
from django.contrib.auth.hashers import make_password

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        # Create default admin user if no user exists
        if not self.db.execute("SELECT COUNT(*) FROM auth_user")[0][0] == 0:
            return
        admin_password = os.environ.get("NOC_DEFAULT_ADMIN_PASSWORD", "admin")
        admin_email = os.environ.get("NOC_DEFAULT_ADMIN_EMAIL", "test@example.com")
        self.db.execute(
            "INSERT INTO auth_user"
            "(username, first_name, last_name, email, password, is_active, is_superuser, date_joined) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, 'now')",
            ["admin", "NOC", "Admin", admin_email, make_password(admin_password), True, True],
        )
