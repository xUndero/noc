# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# failed log expire
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
# NOC modules
from noc.core.migration.base import BaseMigration
from noc.lib.nosql import get_db


class Migration(BaseMigration):
    def migrate(self):
        expires = datetime.datetime.now() + datetime.timedelta(days=7)
        c = get_db()["noc.log.sa.failed_scripts"]
        c.update_many({}, {"$set": {"expires": expires}})
