# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# BaseMigration
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import six


@six.python_2_unicode_compatible
class BaseMigration(object):
    depends_on = []

    def __str__(self):
        return self.get_name()

    @classmethod
    def get_name(cls):
        parts = cls.__module__.split(".")
        return u"%s.%s" % (parts[1], parts[3])

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
