# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Path tracing utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
from collections import defaultdict
import operator

# Third-party modules
import six
from typing import Optional, Iterable, List, Dict, Set, Tuple, DefaultDict, NamedTuple
from bson import ObjectId

# NOC modules
from noc.inv.models.networksegment import NetworkSegment
from noc.inv.models.link import Link
from noc.sa.models.managedobject import ManagedObject
from .goal.base import BaseGoal
from .constraint.base import BaseConstraint

MAX_PATH_LENGTH = 0xFFFFFFFF
PathInfo = NamedTuple(
    "PathInfo",
    [("start", ManagedObject), ("end", ManagedObject), ("links", List[Link]), ("l2_cost", int)],
)


def get_shortest_path(start, goal):
    # type: (ManagedObject, ManagedObject) -> List[ManagedObject]
    """
    Returns a list of Managed Objects along shortest path
    using modified A* algorithm
    :param start: Starting managed object's id
    :param goal: Ending managed object's id
    :return:
    """
    finder = KSPFinder(start, goal)
    for path in finder.find_shortest_path():  # type: PathInfo
        r = []  # type: List[ManagedObject]
        pi = None
        for pi in path:
            r += [pi.start]
        if pi:
            r += [pi.end]
        return r
    raise ValueError("Path not found")


class KSPFinder(object):
    """
    k-Shortest Path finder
    """

    def __init__(self, start, goal, constraint=None, max_depth=MAX_PATH_LENGTH, n_shortest=1):
        # type: (ManagedObject, BaseGoal, Optional[BaseConstraint], Optional[int], Optional[int]) -> None
        self.start = start  # type: ManagedObject
        self.goal = goal  # type: BaseGoal
        self.constraint = constraint  # type: Optional[BaseConstraint]
        self.max_depth = max_depth  # type: Optional[int]
        self.n_shortest = n_shortest  # type: Optional[int]
        # Set of segments on path
        self.segments = set()  # type: Set[NetworkSegment]
        # Managed Object cache
        self.mo_cache = {}  # type: Dict[int, ManagedObject]
        # Links cache
        self.mo_links = {}  # type: Dict[ManagedObject, Set[Link]]

    def find_shortest_path(self):
        # type: () -> List[PathInfo]
        """
        Returns a list of Managed Objects along shortest path
        using modified A* algorithm

        :return:
        """
        return self._find_shortest_path(self.start)

    def _find_shortest_path(self, start, pruned_links=None):
        # type: (ManagedObject, Optional[Set[ObjectId]]) -> List[PathInfo]
        """
        Returns a list of Managed Objects along shortest path
        using modified A* algorithm

        :param pruned_links: Set of links id to be excluded from path calculation
        :return:
        """

        def max_path_length():
            # type: () -> int
            return self.max_depth

        def iter_neighbors(n_ids):
            # type: (Iterable[int]) -> Iterable[ManagedObject]
            for m_id in n_ids:
                n_mo = self.mo_cache.get(m_id)
                if n_mo:
                    yield n_mo
                else:
                    n_mo = ManagedObject.get_by_id(m_id)
                    if n_mo:
                        self.mo_cache[n_mo.id] = n_mo
                        yield n_mo

        def is_allowed_link(current_mo, link):
            # type: (ManagedObject, Link) -> bool
            allow_egress = False
            allow_ingress = False
            for iface in link.interfaces:
                if iface.managed_object.id == current_mo.id:
                    # Egress
                    if not allow_egress:
                        allow_egress = self.constraint.is_valid_egress(iface)
                else:
                    # Ingress
                    if not allow_ingress:
                        allow_ingress = self.constraint.is_valid_ingress(iface)
                if allow_egress and allow_ingress:
                    return True
            return False

        def iter_links(current_mo):
            # type:(ManagedObject) -> Iterable[Link]
            links = self.mo_links.get(current_mo, None)  # type: Optional[Set[Link]]
            if links is None:
                links = set(Link.objects.filter(linked_objects=current_mo.id))
                self.mo_links[current_mo] = links
            for link in links:
                # Prune excluded links
                if pruned_links and link.id in pruned_links:
                    continue
                if not self.constraint or is_allowed_link(current_mo, link):
                    yield link

        def reconstruct_path(goal_mo):
            # type: (ManagedObject) -> List[PathInfo]
            obj_path = [goal_mo]  # type: List[ManagedObject]
            while True:
                goal_mo = came_from.get(goal_mo)
                if not goal_mo:
                    break
                obj_path.insert(0, goal_mo)
            full_path = []  # type: List[PathInfo]
            for mo1, mo2 in six.moves.zip(obj_path, obj_path[1:]):
                links = [link for link in self.mo_links[mo1] if mo2.id in link.linked_objects]
                cost = min(link.l2_cost or 1 for link in links)
                full_path += [PathInfo(mo1, mo2, links, cost)]
            return full_path

        # Already evaluated nodes, contains MO ids
        closed_set = set()  # type: Set[int]
        # Currently discovered nodes than are not evaluated yet.
        # Start node is already known
        open_set = {start}  # type: Set[ManagedObject]
        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, came_from will eventually contain the
        # most efficient previous step.
        came_from = {}  # type: Dict[ManagedObject, ManagedObject]
        # For each node, the cost of getting from the start node to that node.
        # Default value is infinity
        g_score = defaultdict(max_path_length)  # type: DefaultDict[ManagedObject, int]
        # The cost of going from start to start is zero.
        g_score[start] = 0
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        f_score = defaultdict(max_path_length)  # type: Dict[ManagedObject, int]
        # For the first node, that value is completely heuristic.
        f_score[start] = self.goal.cost_estimate(start)
        # Find solution
        while open_set:
            # Current is the node in open_set having the lowest f_score value
            current = sorted(open_set, key=lambda x: f_score[x])[0]
            # If current matches goal, solution found
            if self.goal.is_goal(current):
                return reconstruct_path(current)
            # Move current from open_set to closed_set
            open_set.remove(current)
            closed_set.add(current.id)
            # Get neighbors of current and their distances
            seen_neighbors = set()  # type: Set[int]
            dist = {}  # type: Dict[int, int]
            for l in iter_links(current):
                new_neighbors = (
                    set(l.linked_objects) - closed_set
                )  # Current is already in closed set
                seen_neighbors |= new_neighbors
                for mo in new_neighbors:
                    dist[mo] = min(l.l2_cost, dist.get(mo, MAX_PATH_LENGTH))
            # Evaluate neighbors
            for neighbor in iter_neighbors(seen_neighbors):
                if self.constraint and not self.constraint.is_valid_neighbor(neighbor):
                    continue  # Skip invalid neighbors
                if neighbor not in open_set:
                    open_set.add(neighbor)  # Discover a new node
                # The distance from start to a neighbor
                tentative_g_score = g_score[current] + dist[neighbor.id]
                if tentative_g_score >= g_score[neighbor]:
                    continue  # Not a better path
                # This path is best until now, record it
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.goal.cost_estimate(neighbor, current)
        raise ValueError("Path not found")

    def iter_shortest_paths(self):
        # type: () -> Iterable[List[PathInfo]]
        """
        Returns a list of up to `n_shortest` shortest paths.
        Yen's algorithm applied to A*

        :return:
        """

        def to_path(path):
            # type: (List[PathInfo]) -> List[ManagedObject]
            r = []  # type: List[ManagedObject]
            for pi in path:
                r += [pi.start]
            r += [pi.end]
            return r

        def apply_pruned(path):
            # type: (List[PathInfo]) -> None
            for pi in path:
                for link in pi.links:
                    pruned_links[pi.start].add(link.id)
                    pruned_links[pi.end].add(link.id)

        # Shortcut for one path
        A = self._find_shortest_path(self.start)  # type: List[PathInfo]
        yield A
        if self.n_shortest == 1:
            raise StopIteration
        # Pruned links for each spur node
        pruned_links = defaultdict(set)  # type: DefaultDict[ManagedObject, Set[ObjectId]]
        # Alternative paths
        B = []  # type: List[Tuple[List[PathInfo], int]]
        #
        for k in range(1, self.n_shortest):
            apply_pruned(A)
            a_path = to_path(A)[:-2]
            for i, spur_node in enumerate(a_path):
                root_path = A[:i]
                try:
                    spur_path = self._find_shortest_path(spur_node, pruned_links[spur_node])
                except ValueError:
                    continue
                total_path = root_path + spur_path
                B += [(total_path, sum(pi.l2_cost for pi in total_path))]
            if not B:
                break  # No alternative paths
            # Find best alternative path and add to result
            B = sorted(B, key=operator.itemgetter(1))
            A = B.pop(0)[0]
            yield A
