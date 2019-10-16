# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# path API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
from collections import defaultdict

# Third-party modules
import six
import tornado.gen
import ujson
from typing import Tuple, Optional, Dict, List, Iterable, DefaultDict, Any

# NOC modules
from noc.core.service.apiaccess import authenticated
from noc.sa.interfaces.base import DictParameter, StringParameter, IntParameter, ObjectIdParameter
from noc.main.models.remotesystem import RemoteSystem
from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface
from noc.sa.models.service import Service
from noc.core.span import Span
from noc.core.backport.time import perf_counter
from noc.core.topology.path import KSPFinder, PathInfo
from noc.core.topology.goal.base import BaseGoal
from noc.core.topology.goal.managedobject import ManagedObjectGoal
from noc.core.topology.goal.level import ManagedObjectLevelGoal
from noc.core.text import split_alnum
from ..base import NBIAPI

# Constants
MAX_DEPTH_DEFAULT = 20
N_SHORTEST_DEFAULT = 10

# id/remote system pointer
PointerId = DictParameter(attrs={"id": StringParameter()})
PointerRemote = DictParameter(
    attrs={"remote_system": StringParameter(), "remote_id": StringParameter()}
)
Pointer = PointerId | PointerRemote

# from: section
ObjectPointer = DictParameter(
    attrs={
        "object": Pointer,
        "interface": DictParameter(attrs={"name": StringParameter()}, required=False),
    }
)
InterfacePointer = DictParameter(
    attrs={"interface": DictParameter(attrs={"id": ObjectIdParameter()})}
)
LevelPointer = DictParameter(attrs={"level": IntParameter()})
ServicePointer = DictParameter(attrs={"service": Pointer})
RequestFrom = ObjectPointer | InterfacePointer | ServicePointer
# to: section
RequestTo = ObjectPointer | LevelPointer | InterfacePointer | ServicePointer
# config: section
RequestConfig = DictParameter(
    attrs={
        "max_depth": IntParameter(default=MAX_DEPTH_DEFAULT),
        "n_shortest": IntParameter(default=N_SHORTEST_DEFAULT),
    },
    required=False,
)
RequestConstraints = DictParameter(required=False)
Request = DictParameter(
    attrs={
        "from": RequestFrom,
        "to": RequestTo,
        "config": RequestConfig,
        "constraints": RequestConstraints,
    }
)


class PathAPI(NBIAPI):
    name = "path"

    @authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        code, result = yield self.executor.submit(self.handler)
        self.set_status(code)
        if isinstance(result, six.string_types):
            self.write(result)
        else:
            self.set_header("Content-Type", "text/json")
            self.write(ujson.dumps(result))

    def handler(self):
        # type: () -> Tuple[int, Dict]
        # Decode request
        try:
            req = ujson.loads(self.request.body)
        except ValueError:
            return 400, {"status": False, "error": "Cannot decode JSON"}
        # Validate
        try:
            req = Request.clean(req)
        except ValueError as e:
            return 400, {"status": False, "error": "Bad request: %s" % e}
        # Find start of path
        try:
            with Span(in_label="start_of_path"):
                start, start_iface = self.get_object_and_interface(**req["from"])
        except ValueError as e:
            return 404, {"status": False, "error": "Failed to find start of path: %s" % e}
        # Find end of path
        if "level" in req["to"]:
            goal = ManagedObjectLevelGoal(req["to"]["level"])
            end_iface = None
        else:
            try:
                with Span(in_label="end_of_path"):
                    end, end_iface = self.get_object_and_interface(**req["to"])
                goal = ManagedObjectGoal(end)
            except ValueError as e:
                return 404, {"status": False, "error": "Failed to find end of path: %s" % e}
        # Trace the path
        if req.get("config"):
            max_depth = req["config"]["max_depth"]
            n_shortest = req["config"]["n_shortest"]
        else:
            max_depth = MAX_DEPTH_DEFAULT
            n_shortest = N_SHORTEST_DEFAULT
        error = None
        with Span(in_label="find_path"):
            t0 = perf_counter()
            try:
                paths = list(
                    self.iter_paths(
                        start,
                        start_iface,
                        goal,
                        end_iface,
                        max_depth=max_depth,
                        n_shortest=n_shortest,
                    )
                )
            except ValueError as e:
                error = str(e)
            dt = perf_counter() - t0
        if error:
            return 404, {"status": False, "error": e, "time": dt}
        return 200, {"status": True, "paths": paths, "time": dt}

    def get_object_and_interface(self, object=None, interface=None, service=None):
        # type: (Optional[Dict], Optional[Dict], Optional[Dict], Optional[Dict]) -> Tuple[ManagedObject, Optional[Interface]]
        """
        Process from and to section of request and get object and interface

        :param object: request.object
        :param interface: request.interface
        :param service: request.service

        :return: ManagedObject Instance, Optional[Interface Instance]
        :raises ValueError:
        """
        if object:
            if "id" in object:
                # object.id
                mo = ManagedObject.get_by_id(object["id"])
            elif "remote_system" in object:
                # object.remote_system/remote_id
                rs = RemoteSystem.get_by_id(object["remote_system"])
                if not rs:
                    raise ValueError("Remote System not found")
                mo = ManagedObject.objects.filter(
                    remote_system=rs.id, remote_id=object["remote_id"]
                ).first()
            else:
                raise ValueError("Neither id or remote system specified")
            if not mo:
                raise ValueError("Object not found")
            if interface:
                # Additional interface restriction
                iface = mo.get_interface(interface["name"])
                if iface is None:
                    raise ValueError("Interface not found")
                return mo, iface
            else:
                # No interface restriction
                return mo, None
        if interface:
            iface = Interface.objects.filter(id=interface["id"]).first()
            if not iface:
                raise ValueError("Interface not found")
            return iface.managed_object, iface
        if service:
            if "id" in service:
                svc = Service.objects.filter("id").first()
            elif "remote_system" in service:
                rs = RemoteSystem.get_by_id(object["remote_system"])
                if not rs:
                    raise ValueError("Remote System not found")
                svc = Service.objects.filter(
                    remote_system=rs.id, remote_id=service["remote_id"]
                ).first()
            else:
                raise ValueError("Neither id or remote system specified")
            if svc is None:
                raise ValueError("Service not found")
            iface = Interface.objects.filter(service=svc.id).first()
            if not iface:
                raise ValueError("Interface not found")
            return iface.managed_object, iface
        raise ValueError("Invalid search condition")

    def iter_paths(
        self,
        start,
        start_iface,
        goal,
        end_iface,
        max_depth=MAX_DEPTH_DEFAULT,
        n_shortest=N_SHORTEST_DEFAULT,
    ):
        # type: (ManagedObject, Optional[Interface], BaseGoal, Optional[Interface], int, int) -> Iterable[Dict]
        """
        Iterate possible paths

        :param start: Starting Managed Object
        :param start_iface: Starting interface or None
        :param goal: BaseGoal instance to match end of path
        :param end_iface: Ending interface or None
        :param max_depth: Max search depth
        :param n_shortest: Restrict to `n_shortest` shortest paths
        :return:
        """

        def encode_link(interfaces):
            # type: (List[Interface]) -> Dict
            objects = defaultdict(list)  # type: DefaultDict[ManagedObject, List]
            for iface in interfaces:
                objects[iface.managed_object] += [iface.name]
            # Order objects
            order = list(objects)  # type: List[ManagedObject]
            try:
                idx = order.index(last["obj"])
                o = order.pop(idx)
                order.insert(0, o)
                last["obj"] = order[-1]
            except ValueError:
                pass
            #
            return {
                "objects": [
                    {
                        "object": {
                            "id": obj.id,
                            "name": obj.name,
                            "address": obj.address,
                            "bi_id": obj.bi_id,
                        },
                        "interfaces": list(sorted(objects[obj], key=split_alnum)),
                    }
                    for obj in order
                ]
            }  # type: Dict[str, Any]

        finder = KSPFinder(start, goal, max_depth=max_depth, n_shortest=n_shortest)
        for path in finder.iter_shortest_paths():  # type: List[PathInfo]
            last = {"obj": start}  # type: Dict[str, ManagedObject]
            r = {"path": [], "cost": {"l2": 0}}
            if start_iface:
                r["path"] += [{"links": [encode_link([start_iface])]}]
            for pi in path:  # type: PathInfo
                r["path"] += [{"links": [encode_link(link.interfaces) for link in pi.links]}]
                r["cost"]["l2"] += pi.l2_cost
            if end_iface:
                r["path"] += [{"links": [encode_link([end_iface])]}]
            yield r
