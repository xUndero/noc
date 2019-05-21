# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# cleanup
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):

    depends_on = (("sa", "0003_task_schedule"),)

    def migrate(self):
        db.execute(
            "UPDATE sa_taskschedule SET periodic_name='main.cleanup' WHERE periodic_name='main.cleanup_sessions'"
        )
