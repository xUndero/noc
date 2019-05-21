# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# BaseMigration
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


class BaseMigration(object):
    depends_on = []

    def migrate(self):
        """
        Actual migration code
        :return:
        """
        pass

    def forwards(self):
        """
        South-compatible method
        :return:
        """
        self.migrate()

    def backwards(self):
        """
        South-compatible method
        :return:
        """
        pass
