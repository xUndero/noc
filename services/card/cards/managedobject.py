# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ManagedObject card handler
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
from collections import OrderedDict
import datetime
import operator

# Third-party modules
import six
from django.db.models import Q
from mongoengine.errors import DoesNotExist

# NOC modules
from .base import BaseCard
from noc.sa.models.managedobject import ManagedObject, ManagedObjectAttribute
from noc.fm.models.activealarm import ActiveAlarm
from noc.sa.models.servicesummary import SummaryItem
from noc.fm.models.uptime import Uptime
from noc.fm.models.outage import Outage
from noc.inv.models.object import Object
from noc.inv.models.resourcegroup import ResourceGroup
from noc.inv.models.discoveryid import DiscoveryID
from noc.inv.models.interface import Interface
from noc.inv.models.link import Link
from noc.sa.models.service import Service
from noc.inv.models.firmwarepolicy import FirmwarePolicy
from noc.sa.models.servicesummary import ServiceSummary
from noc.core.text import split_alnum, list_to_ranges
from noc.maintenance.models.maintenance import Maintenance
from noc.sa.models.useraccess import UserAccess
from noc.core.pm.utils import get_interface_metrics, get_objects_metrics
from noc.pm.models.metrictype import MetricType
from noc.core.perf import metrics


class ManagedObjectCard(BaseCard):
    name = "managedobject"
    default_template_name = "managedobject"
    model = ManagedObject

    def get_object(self, id):
        if self.current_user.is_superuser:
            return ManagedObject.objects.get(id=id)
        else:
            return ManagedObject.objects.get(
                id=id, administrative_domain__in=self.get_user_domains()
            )

    def get_template_name(self):
        return self.object.object_profile.card or "managedobject"

    # get data function
    def get_data(self):
        def sortdict(dct):
            kys = dct.keys()
            kys.sort()
            res = OrderedDict()
            for x in kys:
                for k, v in dct.iteritems():
                    if k == x:
                        res[k] = v
            return res

        def get_container_path(self):
            # Get container path
            if not self.object:
                return None
            cp = []
            if self.object.container:
                c = self.object.container.id
                while c:
                    try:
                        o = Object.objects.get(id=c)
                        # @todo: Address data
                        if o.container:
                            cp.insert(0, {"id": o.id, "name": o.name})
                        c = o.container.id if o.container else None
                    except DoesNotExist:
                        metrics["error", ("type", "no_such_object")] += 1
                        break
            return cp

        if not self.object:
            return None
        # @todo: Stage
        # @todo: Service range
        # @todo: Open TT
        now = datetime.datetime.now()
        # Get object status and uptime

        alarms = list(ActiveAlarm.objects.filter(managed_object=self.object.id))

        current_start = None
        duration = None
        if self.object.is_managed:
            if self.object.get_status():
                if alarms:
                    current_state = "alarm"
                else:
                    current_state = "up"
                uptime = Uptime.objects.filter(object=self.object.id, stop=None).first()
                if uptime:
                    current_start = uptime.start
            else:
                current_state = "down"
                outage = Outage.objects.filter(object=self.object.id, stop=None).first()
                if outage is not None:
                    current_start = outage.start
        else:
            current_state = "unmanaged"
        if current_start:
            duration = now - current_start

        cp = get_container_path(self)

        # MAC addresses
        macs = []
        o_macs = DiscoveryID.macs_for_object(self.object)
        if o_macs:
            for f, l in o_macs:
                if f == l:
                    macs += [f]
                else:
                    macs += ["%s - %s" % (f, l)]

        # Links
        uplinks = set(self.object.data.uplinks)
        if len(uplinks) > 1:
            if self.object.segment.lost_redundancy:
                redundancy = "L"
            else:
                redundancy = "R"
        else:
            redundancy = "N"
        links = []
        for l in Link.object_links(self.object):
            local_interfaces = []
            remote_interfaces = []
            remote_objects = set()
            for i in l.interfaces:
                if i.managed_object.id == self.object.id:
                    local_interfaces += [i]
                else:
                    remote_interfaces += [i]
                    remote_objects.add(i.managed_object)
            if len(remote_objects) == 1:
                ro = remote_objects.pop()
                if ro.id in uplinks:
                    role = "uplink"
                else:
                    role = "downlink"
                links += [
                    {
                        "id": l.id,
                        "role": role,
                        "local_interface": sorted(
                            local_interfaces, key=lambda x: split_alnum(x.name)
                        ),
                        "remote_object": ro,
                        "remote_interface": sorted(
                            remote_interfaces, key=lambda x: split_alnum(x.name)
                        ),
                        "remote_status": "up" if ro.get_status() else "down",
                    }
                ]
            links = sorted(
                links,
                key=lambda x: (x["role"] != "uplink", split_alnum(x["local_interface"][0].name)),
            )
        # Build global services summary
        service_summary = ServiceSummary.get_object_summary(self.object)

        # Interfaces
        interfaces = []
        metrics_map = [
            "Interface | Load | In",
            "Interface | Load | Out",
            "Interface | Errors | In",
            "Interface | Errors | Out",
        ]

        mo = ManagedObject.objects.filter(id=self.object.id)

        ifaces_metrics, last_ts = get_interface_metrics(mo[0])
        ifaces_metrics = ifaces_metrics[mo[0]]

        objects_metrics, last_time = get_objects_metrics(mo[0])
        objects_metrics = objects_metrics.get(mo[0])

        meta = {}
        metric_type_name = dict(MetricType.objects.filter().scalar("name", "measure"))
        metric_type_field = dict(MetricType.objects.filter().scalar("field_name", "measure"))
        if objects_metrics:
            for path, mres in six.iteritems(objects_metrics):
                for key in mres:
                    metric_name = "%s | %s" % (key, path) if any(path.split("|")) else key
                    meta[metric_name] = {"type": metric_type_name[key], "value": mres[key]}

        for i in Interface.objects.filter(managed_object=self.object.id, type="physical"):
            load_in = "-"
            load_out = "-"
            errors_in = "-"
            errors_out = "-"
            iface_metrics = ifaces_metrics.get(str(i.name))
            if iface_metrics:
                for key, value in six.iteritems(iface_metrics):
                    if key not in metrics_map:
                        continue
                    metric_type = metric_type_name.get(key) or metric_type_field.get(key)
                    if key == "Interface | Load | In":
                        load_in = (
                            "%s%s" % (self.humanize_speed(value, metric_type), metric_type)
                            if value
                            else "-"
                        )
                    if key == "Interface | Load | Out":
                        load_out = (
                            "%s%s" % (self.humanize_speed(value, metric_type), metric_type)
                            if value
                            else "-"
                        )
                    if key == "Interface | Errors | In":
                        errors_in = value if value else "-"
                    if key == "Interface | Errors | Out":
                        errors_out = value if value else "-"
            interfaces += [
                {
                    "id": i.id,
                    "name": i.name,
                    "admin_status": i.admin_status,
                    "oper_status": i.oper_status,
                    "mac": i.mac or "",
                    "full_duplex": i.full_duplex,
                    "load_in": load_in,
                    "load_out": load_out,
                    "errors_in": errors_in,
                    "errors_out": errors_out,
                    "speed": max([i.in_speed or 0, i.out_speed or 0]) / 1000,
                    "untagged_vlan": None,
                    "tagged_vlan": None,
                    "profile": i.profile,
                    "service": i.service,
                    "service_summary": service_summary.get("interface").get(i.id, {}),
                    "description": i.description,
                }
            ]

            si = list(i.subinterface_set.filter(enabled_afi="BRIDGE"))
            if len(si) == 1:
                si = si[0]
                interfaces[-1]["untagged_vlan"] = si.untagged_vlan
                interfaces[-1]["tagged_vlans"] = list_to_ranges(si.tagged_vlans).replace(",", ", ")
        interfaces = sorted(interfaces, key=lambda x: split_alnum(x["name"]))
        # Resource groups
        # Service groups (i.e. server)
        static_services = set(self.object.static_service_groups)
        service_groups = []
        for rg_id in self.object.effective_service_groups:
            rg = ResourceGroup.get_by_id(rg_id)
            service_groups += [
                {
                    "id": rg_id,
                    "name": rg.name,
                    "technology": rg.technology,
                    "is_static": rg_id in static_services,
                }
            ]
        # Client groups (i.e. client)
        static_clients = set(self.object.static_client_groups)
        client_groups = []
        for rg_id in self.object.effective_client_groups:
            rg = ResourceGroup.get_by_id(rg_id)
            client_groups += [
                {
                    "id": rg_id,
                    "name": rg.name,
                    "technology": rg.technology,
                    "is_static": rg_id in static_clients,
                }
            ]
        # @todo: Administrative domain path
        # Alarms
        alarm_list = []
        for a in alarms:
            alarm_list += [
                {
                    "id": a.id,
                    "root_id": self.get_root(alarms),
                    "timestamp": a.timestamp,
                    "duration": now - a.timestamp,
                    "subject": a.subject,
                    "managed_object": a.managed_object,
                    "service_summary": {
                        "service": SummaryItem.items_to_dict(a.total_services),
                        "subscriber": SummaryItem.items_to_dict(a.total_subscribers),
                    },
                    "alarm_class": a.alarm_class,
                }
            ]
        alarm_list = sorted(alarm_list, key=operator.itemgetter("timestamp"))

        # Maintenance
        maintenance = []
        for m in Maintenance.objects.filter(
            affected_objects__object=self.object.id,
            is_completed=False,
            start__lte=now + datetime.timedelta(hours=1),
        ):
            maintenance += [
                {
                    "maintenance": m,
                    "id": m.id,
                    "subject": m.subject,
                    "start": m.start,
                    "stop": m.stop,
                    "in_progress": m.start <= now,
                }
            ]
        # Get Inventory
        inv = []
        for p in self.object.get_inventory():
            c = self.get_nested_inventory(p)
            c["name"] = p.name or self.object.name
            inv += [c]
        # Build result

        if self.object.platform is not None:
            platform = self.object.platform.name
        else:
            platform = "Unknown"
        if self.object.version is not None:
            version = self.object.version.version
        else:
            version = ""

        r = {
            "id": self.object.id,
            "object": self.object,
            "name": self.object.name,
            "address": self.object.address,
            "platform": platform,
            # self.object.platform.name if self.object.platform else "Unknown",
            "version": version,
            # self.object.version.version if self.object.version else "",
            "description": self.object.description,
            "object_profile": self.object.object_profile.id,
            "object_profile_name": self.object.object_profile.name,
            "macs": ", ".join(sorted(macs)),
            "segment": self.object.segment,
            "firmware_status": FirmwarePolicy.get_status(self.object.platform, self.object.version),
            "firmware_recommended": FirmwarePolicy.get_recommended_version(self.object.platform),
            "service_summary": service_summary,
            "container_path": cp,
            "current_state": current_state,
            # Start of uptime/downtime
            "current_start": current_start,
            # Current uptime/downtime
            "current_duration": duration,
            "service_groups": service_groups,
            "client_groups": client_groups,
            "tt": [],
            "links": links,
            "alarms": alarm_list,
            "interfaces": interfaces,
            "metrics": sortdict(meta),
            "maintenance": maintenance,
            "redundancy": redundancy,
            "inventory": self.flatten_inventory(inv),
            "serial_number": self.object.get_attr("Serial Number"),
            "attributes": list(
                ManagedObjectAttribute.objects.filter(managed_object=self.object.id)
            ),
            "confdb": None,
        }
        try:
            r["confdb"] = self.object.get_confdb()
        except SyntaxError:
            pass
        return r

    def get_service_glyphs(self, service):
        """
        Returns a list of (service profile name, glyph)
        """
        r = []
        if service.logical_status in ("T", "R", "S"):
            if service.profile.glyph:
                r += [(service.profile.name, service.profile.glyph)]
            for svc in Service.objects.filter(parent=service):
                r += self.get_service_glyphs(svc)
        return r

    @classmethod
    def search(cls, handler, query):
        q = Q(name__icontains=query)
        sq = ManagedObject.get_search_Q(query)
        if sq:
            q |= sq
        if not handler.current_user.is_superuser:
            q &= UserAccess.Q(handler.current_user)
        r = []
        for mo in ManagedObject.objects.filter(q):
            r += [
                {
                    "scope": "managedobject",
                    "id": mo.id,
                    "label": "%s (%s) [%s]" % (mo.name, mo.address, mo.platform),
                }
            ]
        return r

    def get_nested_inventory(self, o):
        rev = o.get_data("asset", "revision")
        if rev == "None":
            rev = ""
        r = {
            "id": str(o.id),
            "serial": o.get_data("asset", "serial"),
            "revision": rev or "",
            "description": o.model.description,
            "model": o.model.name,
            "children": [],
        }
        for n in o.model.connections:
            if n.direction == "i":
                c, r_object, _ = o.get_p2p_connection(n.name)
                if c is None:
                    r["children"] += [
                        {
                            "id": "",
                            "name": n.name,
                            "serial": "",
                            "description": "--- EMPTY ---",
                            "model": "",
                        }
                    ]
                else:
                    cc = self.get_nested_inventory(r_object)
                    cc["name"] = n.name
                    r["children"] += [cc]
            elif n.direction == "s":
                r["children"] += [
                    {
                        "id": "",
                        "name": n.name,
                        "serial": "",
                        "description": n.description,
                        "model": ", ".join(n.protocols),
                    }
                ]
        return r

    def flatten_inventory(self, inv, level=0):
        r = []
        if not isinstance(inv, list):
            inv = [inv]
        for o in inv:
            r += [o]
            o["level"] = level
            children = o.get("children", [])
            if children:
                for c in children:
                    r += self.flatten_inventory(c, level + 1)
                del o["children"]
        return r

    @staticmethod
    def humanize_speed(speed, type_speed):
        def func_to_bytes(speed):
            try:
                speed = float(speed)
            except ValueError:
                pass
                # speed = speed / 8.0
            if speed < 1024:
                return speed
            for t, n in [(pow(2, 30), "G"), (pow(2, 20), "M"), (pow(2, 10), "k")]:
                if speed >= t:
                    if speed // t * t == speed:
                        return "%d% s" % (speed // t, n)
                    else:
                        return "%.2f %s" % (float(speed) / t, n)

        def func_to_bit(speed):
            if not speed:
                return "-"
            try:
                speed = int(speed)
            except ValueError:
                pass
            if speed < 1000 and speed > 0:
                return "%s " % speed
            for t, n in [(1000000000, "G"), (1000000, "M"), (1000, "k")]:
                if speed >= t:
                    if speed // t * t == speed:
                        return "%d&nbsp;%s" % (speed // t, n)
                    else:
                        return "%.2f&nbsp;%s" % (float(speed) / t, n)

        def func_to_bool(speed):
            return bool(speed)

        result = speed
        if not speed:
            result = "-"
        try:
            speed = int(speed)
        except ValueError:
            pass
        if type_speed == "bit/s":
            result = func_to_bit(speed)
        if type_speed == "bytes":
            result = func_to_bytes(speed)
        if type_speed == "bool":
            result = func_to_bool(speed)
        if result == speed:
            result = speed
        return result

    @staticmethod
    def get_root(_root):
        for value in _root:
            if value.root is not None:
                return value.root
