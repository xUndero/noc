# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event log
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration

EVENT_STATUS_CHOICES = [("U", "Unclassified"), ("A", "Active"), ("C", "Closed")]


class Migration(BaseMigration):
    def migrate(self):
        # Mock Models
        Event = self.db.mock_model(
            model_name='Event',
            db_table='fm_event',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # Model 'EventLog'
        self.db.create_table(
            'fm_eventlog', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('event', models.ForeignKey(Event, verbose_name=Event)),
                ('timestamp', models.DateTimeField("Timestamp")),
                ('from_status', models.CharField("From Status", max_length=1, choices=EVENT_STATUS_CHOICES)),
                ('to_status', models.CharField("To Status", max_length=1, choices=EVENT_STATUS_CHOICES)),
                ('message', models.TextField("Message"))
            )
        )
