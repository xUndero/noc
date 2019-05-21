# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# checkpoint
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        User = self.db.mock_model(
            model_name="User",
            db_table="auth_user",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )

        self.db.create_table(
            "main_checkpoint", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("timestamp", models.DateTimeField("Timestamp")),
                ("user", models.ForeignKey(User, verbose_name="User", blank=True, null=True)),
                ("comment", models.CharField("Comment", max_length=256)),
                ("private", models.BooleanField("Private", default=False))
            )
        )
