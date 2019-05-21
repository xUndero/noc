# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# postprocessing rule params
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

    depends_on = (("main", "0015_notification_link"),)

    def migrate(self):
        ManagedObjectSelector = db.mock_model(
            model_name='ManagedObjectSelector',
            db_table='sa_managedobjectselector',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        TimePattern = db.mock_model(
            model_name='TimePattern',
            db_table='main_timepattern',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        NotificationGroup = db.mock_model(
            model_name='NotificationGroup',
            db_table='main_notificationgroup',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        db.add_column(
            "fm_eventpostprocessingrule", "managed_object_selector",
            models.ForeignKey(ManagedObjectSelector, verbose_name="Managed Object Selector", null=True, blank=True)
        )
        db.add_column(
            "fm_eventpostprocessingrule", "time_pattern",
            models.ForeignKey(TimePattern, verbose_name="Time Pattern", null=True, blank=True)
        )
        db.add_column(
            "fm_eventpostprocessingrule", "notification_group",
            models.ForeignKey(NotificationGroup, verbose_name="Notification Group", null=True, blank=True)
        )
