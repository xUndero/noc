# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Vendor attributes to collection
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import uuid
from south.db import db
# NOC modules
from noc.core.model.fields import DocumentReferenceField
from noc.lib.nosql import get_db

OLD_VENDOR_MAP = {
    "Alcatel-Lucent": "ALU",
    "Arista Networks": "ARISTA",
    "Edge-Core": "EDGECORE",
    "Cisco Networks": "CISCO",
    "D-Link": "DLINK",
    "Extreme Networks": "EXTREME",
    "f5 Networks": "F5",
    "Force10 Networks": "FORCE10",
    "Huawei Technologies Co.": "HUAWEI",
    "HP": "HP",
    "Juniper Networks": "JUNIPER",
    "NOC": "NOC",
    "NoName": "NONAME",
    "ZTE": "ZTE",
    "ZyXEL": "ZYXEL"
}


class Migration(object):
    def forwards(self):
        #
        # Vendor
        #

        # Select vendors
        vendors = set(r[0] for r in db.execute(
            "SELECT DISTINCT value FROM sa_managedobjectattribute WHERE key = 'vendor'"))
        # Create vendors records
        pcoll = get_db()["noc.vendors"]
        inventory_vendors = {}
        for v in pcoll.find():
            if "code" in v:
                inventory_vendors[v["code"][0] if isinstance(v["code"], list) else v["code"]] = v["_id"]
            elif v["name"] in OLD_VENDOR_MAP:
                inventory_vendors[OLD_VENDOR_MAP[v["name"]]] = v["_id"]
            else:
                inventory_vendors[v["name"].split(" ")[0].upper()] = v["_id"]
        for v in vendors.union(set(inventory_vendors)):
            u = uuid.uuid4()
            vc = v.upper()
            if v in inventory_vendors:
                pcoll.update_one({
                    "_id": inventory_vendors[v]
                }, {
                    "$set": {
                        "code": vc,
                        "uuid": u
                    }
                })
            else:
                pcoll.update_one({
                    "code": vc
                }, {
                    "$set": {
                        "code": vc
                    },
                    "$setOnInsert": {
                        "name": v,
                        "uuid": u
                    }
                }, upsert=True)
        # Get vendor record mappings
        vmap = {}  # name -> id
        for d in pcoll.find({}, {"_id": 1, "code": 1}):
            vmap[d["code"]] = str(d["_id"])
        # Create .vendor field
        db.add_column(
            "sa_managedobject",
            "vendor",
            DocumentReferenceField(
                "inv.Vendor", null=True, blank=True
            )
        )
        # Migrate profile data
        for v in vendors:
            db.execute("""
                UPDATE sa_managedobject
                SET vendor = %s
                WHERE
                  id IN (
                    SELECT managed_object_id
                    FROM sa_managedobjectattribute
                    WHERE
                      key = 'vendor'
                      AND value = %s
                  )
            """, [vmap[v.upper()], v])

    def backwards(self):
        pass
