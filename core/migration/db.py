# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Migration db property
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db as south_db


class DB(object):
    """
    PostgreSQL database migration operations
    """
    def create_table(self, name, fields):
        south_db.create_table(name, fields)

    def delete_table(self, name):
        south_db.delete_table(name)

    def add_column(self, table_name, field_name, field_def):
        south_db.add_column(table_name, field_name, field_def)

    def delete_column(self, table_name, field_name):
        south_db.delete_column(table_name, field_name)

    def execute(self, query, *args):
        return south_db.execute(query, *args)

    def create_index(self, table_name, fields, unique=False, db_tablespace=""):
        south_db.create_index(table_name, fields, unique=unique, db_tablespace=db_tablespace)


# Singleton
db = DB()
