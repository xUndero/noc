# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# bookmarks
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
        # Mock Models
        KBEntry = self.db.mock_model(
            model_name="KBEntry",
            db_table="kb_kbentry",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )

        # Model "KBGlobalBookmark"
        self.db.create_table(
            "kb_kbglobalbookmark", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("kb_entry", models.ForeignKey(KBEntry, verbose_name=KBEntry, unique=True))
            )
        )

        # Mock Models
        User = self.db.mock_model(
            model_name="User",
            db_table="auth_user",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        KBEntry = self.db.mock_model(
            model_name="KBEntry",
            db_table="kb_kbentry",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )

        # Model "KBUserBookmark"
        self.db.create_table(
            "kb_kbuserbookmark", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("user", models.ForeignKey(User, verbose_name=User)),
                ("kb_entry", models.ForeignKey(KBEntry, verbose_name=KBEntry))
            )
        )
        self.db.create_index("kb_kbuserbookmark", ["user_id", "kb_entry_id"], unique=True)
