# -*- coding: utf8 -*-
# ---------------------------------------------------------------------
# inv.reportinterfacestatus
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging
import datetime
import csv

# Third-party modules
from six import StringIO
from django.http import HttpResponse
from pymongo import ReadPreference
from bson import ObjectId
import xlsxwriter

# NOC modules
from noc.lib.app.extapplication import ExtApplication, view
from noc.inv.models.interfaceprofile import InterfaceProfile
from noc.inv.models.interface import Interface
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.managedobjectselector import ManagedObjectSelector
from noc.sa.models.administrativedomain import AdministrativeDomain
from noc.sa.models.useraccess import UserAccess
from noc.core.translation import ugettext as _
from noc.sa.interfaces.base import StringParameter
from noc.core.text import list_to_ranges

logger = logging.getLogger(__name__)


def get_column_width(name):
    excel_column_format = {
        "ID": 6,
        "OBJECT_NAME": 38,
        "OBJECT_STATUS": 10,
        "OBJECT_PROFILE": 17,
        "OBJECT_PLATFORM": 25,
        "AVAIL": 6,
        "ADMIN_DOMAIN": 25,
        "PHYS_INTERFACE_COUNT": 5,
    }
    if name.startswith("Up") or name.startswith("Down") or name.startswith("-"):
        return 8
    elif name.startswith("ADM_PATH"):
        return excel_column_format["ADMIN_DOMAIN"]
    elif name in excel_column_format:
        return excel_column_format[name]
    return 15


class ReportInterfaceStatus(object):
    """Report interface status."""

    def __init__(self, mo_ids, zero, def_profile, interface_profile):
        self.mo_ids = mo_ids
        self.out = self.load(mo_ids, zero, def_profile, interface_profile)

    @staticmethod
    def load(mo_ids, zero, def_profile, interface_profile):
        match = {
            "managed_object": {"$in": mo_ids},
            "type": {"$in": ["physical"]},
            "admin_status": True,
        }

        if interface_profile:
            match["profile"] = {"$in": [ObjectId(str(interface_profile))]}

        if zero:
            match["oper_status"] = True

        if def_profile and interface_profile is None:
            def_prof = [pr.id for pr in InterfaceProfile.objects.filter(name__contains="default")]
            match["profile"] = {"$nin": def_prof}
        lookup = {
            "from": "noc.subinterfaces",
            "localField": "_id",
            "foreignField": "interface",
            "as": "subs",
        }
        result = (
            Interface._get_collection()
            .with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
            .aggregate([{"$match": match}, {"$lookup": lookup}])
        )
        return result

    def __getitem__(self, item):
        return self.out.get(item, [])


class ReportInterfaceStatusApplication(ExtApplication):
    menu = _("Reports") + "|" + _("Interface Status")
    title = _("Interface Status")

    @view(
        "^download/$",
        method=["GET"],
        access="launch",
        api=True,
        validate={
            "administrative_domain": StringParameter(required=False),
            "interface_profile": StringParameter(required=False),
            "selector": StringParameter(required=False),
            "zero": StringParameter(required=False),
            "def_profile": StringParameter(required=False),
            "columns": StringParameter(required=False),
            "o_format": StringParameter(choices=["csv", "xlsx"]),
        },
    )
    def api_report(
        self,
        request,
        o_format,
        administrative_domain=None,
        selector=None,
        interface_profile=None,
        zero=None,
        def_profile=None,
        columns=None,
        enable_autowidth=False,
    ):
        def humanize_speed(speed):
            if not speed:
                return "-"
            for t, n in [(1000000, "G"), (1000, "M"), (1, "k")]:
                if speed >= t:
                    if speed // t * t == speed:
                        return "%d%s" % (speed // t, n)
                    else:
                        return "%.2f%s" % (float(speed) / t, n)
            return str(speed)

        def row(row):
            def qe(v):
                if v is None:
                    return ""
                if isinstance(v, unicode):
                    return v.encode("utf-8")
                elif isinstance(v, datetime.datetime):
                    return v.strftime("%Y-%m-%d %H:%M:%S")
                elif not isinstance(v, str):
                    return str(v)
                else:
                    return v

            return [qe(x) for x in row]

        def translate_row(row, cmap):
            return [row[i] for i in cmap]

        cols = [
            "object_name",
            "object_address",
            "object_model",
            "object_software",
            "object_port_name",
            "object_port_profile_name",
            "object_port_status",
            "object_link_status",
            "object_port_speed",
            "object_port_duplex",
            "object_port_untagged_vlan",
            "object_port_tagged_vlans",
        ]

        header_row = [
            "MANAGED_OBJECT",
            "OBJECT_ADDRESS",
            "OBJECT_MODEL",
            "OBJECT_SOFTWARE",
            "PORT_NAME",
            "PORT_PROFILE_NAME",
            "PORT_STATUS",
            "LINK_STATUS",
            "PORT_SPEED",
            "PORT_DUPLEX",
            "PORT_UNTAGGED_VLAN",
            "PORT_TAGGED_VLANS",
        ]

        if columns:
            cmap = []
            for c in columns.split(","):
                try:
                    cmap += [cols.index(c)]
                except ValueError:
                    continue
        else:
            cmap = list(range(len(cols)))

        r = [translate_row(header_row, cmap)]
        mo = {}
        if_p = {}
        DUPLEX = {True: "Full", False: "Half"}

        for ifp in InterfaceProfile.objects.filter():
            if_p[ifp.id] = {"name": ifp.name}
        mos = ManagedObject.objects.filter(is_managed=True)
        if (
            request.user.is_superuser
            and not administrative_domain
            and not selector
            and not interface_profile
        ):
            mos = ManagedObject.objects.filter(is_managed=True)
        if not request.user.is_superuser:
            mos = mos.filter(administrative_domain__in=UserAccess.get_domains(request.user))
        if administrative_domain:
            ads = AdministrativeDomain.get_nested_ids(int(administrative_domain))
            mos = mos.filter(administrative_domain__in=ads)
        if selector:
            selector = ManagedObjectSelector.get_by_id(int(selector))
            mos = mos.filter(selector.Q)

        for o in mos:
            mo[o.id] = {
                "type": "managedobject",
                "id": str(o.id),
                "name": o.name,
                "status": o.is_managed,
                "address": o.address,
                "vendor": o.vendor,
                "version": o.version,
                "platform": o.platform,
            }

        mos_id = list(mos.values_list("id", flat=True))

        rld = ReportInterfaceStatus(mos_id, zero, def_profile, interface_profile)

        for i in rld.out:
            untag, tagged = "", ""
            if i["subs"]:
                untag = i["subs"][0].get("untagged_vlan", "")
                tagged = list_to_ranges(i["subs"][0].get("tagged_vlans", []))
            r += [
                translate_row(
                    row(
                        [
                            mo[i["managed_object"]]["name"],
                            mo[i["managed_object"]]["address"],
                            "%s %s"
                            % (
                                str(mo[i["managed_object"]]["vendor"]),
                                str(mo[i["managed_object"]]["platform"]),
                            ),
                            str(mo[i["managed_object"]]["version"]),
                            i["name"],
                            if_p[i["profile"]]["name"],
                            "UP" if i["admin_status"] is True else "Down",
                            "UP" if "oper_status" in i and i["oper_status"] is True else "Down",
                            humanize_speed(i["in_speed"]) if "in_speed" in i else "-",
                            DUPLEX.get(i["full_duplex"])
                            if "full_duplex" in i and "in_speed" in i
                            else "-",
                            untag,
                            tagged,
                        ]
                    ),
                    cmap,
                )
            ]

        filename = "interface_status_report_%s" % datetime.datetime.now().strftime("%Y%m%d")
        if o_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="%s.csv"' % filename
            writer = csv.writer(response, dialect="excel", delimiter=";")
            writer.writerows(r)
            return response
        elif o_format == "xlsx":
            response = StringIO()
            wb = xlsxwriter.Workbook(response)
            cf1 = wb.add_format({"bottom": 1, "left": 1, "right": 1, "top": 1})
            ws = wb.add_worksheet("Objects")
            max_column_data_length = {}
            for rn, x in enumerate(r):
                for cn, c in enumerate(x):
                    if rn and (
                        r[0][cn] not in max_column_data_length
                        or len(str(c)) > max_column_data_length[r[0][cn]]
                    ):
                        max_column_data_length[r[0][cn]] = len(str(c))
                    ws.write(rn, cn, c, cf1)
            ws.autofilter(0, 0, rn, cn)
            ws.freeze_panes(1, 0)
            for cn, c in enumerate(r[0]):
                # Set column width
                width = get_column_width(c)
                if enable_autowidth and width < max_column_data_length[c]:
                    width = max_column_data_length[c]
                ws.set_column(cn, cn, width=width)
            wb.close()
            response.seek(0)
            response = HttpResponse(response.getvalue(), content_type="application/vnd.ms-excel")
            # response = HttpResponse(
            #     content_type="application/x-ms-excel")
            response["Content-Disposition"] = 'attachment; filename="%s.xlsx"' % filename
            response.close()
            return response
