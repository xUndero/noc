# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ./noc ch-policy command
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import print_function
from collections import namedtuple, defaultdict
import six
import datetime
# NOC modules
from noc.config import config
from noc.core.management.base import BaseCommand
from noc.core.clickhouse.connect import connection
from noc.main.models.chpolicy import CHPolicy

PartInfo = namedtuple("PartInfo", ["name", "rows", "bytes", "min_date", "max_date"])


class Command(BaseCommand):
    help = "Apply ClickHouse policies"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="cmd")
        # get
        apply_parser = subparsers.add_parser("apply")
        apply_parser.add_argument(
            "--host",
            dest="host",
            help="ClickHouse address"
        )
        apply_parser.add_argument(
            "--port",
            dest="port",
            type=int,
            help="ClickHouse port"
        )
        apply_parser.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Do not apply changes"
        )

    def handle(self, cmd, *args, **options):
        getattr(self, "handle_%s" % cmd)(*args, **options)

    def handle_apply(self, host=None, port=None, dry_run=False, *args, **options):
        read_only = dry_run
        ch = connection(host, port, read_only=read_only)
        today = datetime.date.today()
        # Get partitions
        parts = self.get_parts(ch)
        #
        claimed_bytes = 0
        for p in CHPolicy.objects.filter(is_active=True).order_by("table"):
            table_claimed = 0
            if not p.ttl:
                continue  # Disabled
            deadline = today - datetime.timedelta(days=p.ttl)
            is_dry = dry_run or p.dry_run
            self.print("# Table %s deadline %s%s" % (
                p.table, deadline.isoformat(), " (Dry Run)" if is_dry else ""))
            for pn, pt in six.iteritems(parts[p.table]):
                if pt["max_date"] >= deadline:
                    continue
                self.print("[%s]  Removing partition %s (%s -- %s, %d rows, %d bytes)" % (
                    p.table, pn, pt["min_date"], pt["max_date"], pt["rows"], pt["bytes"]))
                table_claimed += pt["bytes"]
                if not is_dry:
                    ch.execute("ALTER TABLE %s.%s DROP PARTITION '%s'" % (config.clickhouse.db, p.table, pn))
            self.print("  Total %d bytes to be reclaimed" % table_claimed)
            claimed_bytes += table_claimed
        self.print("# Done. %d bytes to be reclaimed" % claimed_bytes)

    def get_parts(self, connect):
        """
        Get partition info
        :param connect:
        :return:
        """
        partitions = defaultdict(dict)
        for row in connect.execute("""
          SELECT table, partition, name, rows, bytes, min_date, max_date
          FROM system.parts
          WHERE
            level > 0
            AND active = 1
            AND database = %s
          ORDER BY table, name
        """, args=(config.clickhouse.db,)
        ):
            if row[1] not in partitions[row[0]]:
                partitions[row[0]][row[1]] = {
                    "min_date": datetime.date(*[int(x) for x in row[5].split("-")]),
                    "max_date": datetime.date(*[int(x) for x in row[6].split("-")]),
                    "rows": int(row[3]),
                    "bytes": int(row[4])
                }
            else:
                partitions[row[0]][row[1]]["max_date"] = datetime.date(*[int(x) for x in row[6].split("-")])
                partitions[row[0]][row[1]]["rows"] += int(row[3])
                partitions[row[0]][row[1]]["bytes"] += int(row[4])
        return partitions


if __name__ == "__main__":
    Command().run()
