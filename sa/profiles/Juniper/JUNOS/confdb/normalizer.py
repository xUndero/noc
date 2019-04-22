# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Juniper.JunOS config normalizer
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.confdb.normalizer.base import BaseNormalizer, match, ANY, REST, deferable


class JunOSNormalizer(BaseNormalizer):

    @match("interfaces", ANY)
    def normalize_interface(self, tokens):
        if_name = self.interface_name(tokens[1])
        yield self.make_interface(interface=self.interface_name(if_name))
        yield self.make_switchport_untagged(
            interface=if_name,
            unit=if_name,
            vlan_filter=1
        )

    @match("interfaces", ANY, "description", REST)
    def normalize_interface_description(self, tokens):
        yield self.make_interface_description(
            interface=self.interface_name(tokens[1]),
            description=" ".join(tokens[3:])
        )

    @match("interfaces", ANY, "unit", ANY, "description", REST)
    def normalize_sub_interface_description(self, tokens):
        if_name = "%s.%s" % (self.interface_name(tokens[1]), tokens[3])
        yield self.defer(
            "fi.iface.%s" % self.interface_name(if_name),
            self.make_unit_description,
            instance=deferable("instance"),
            interface=self.interface_name(if_name),
            unit=self.interface_name(if_name),
            description=" ".join(tokens[5:])
        )

    @match("interfaces", ANY, "unit", ANY, "family", "inet", "address", ANY)
    def normalize_vlan_ip(self, tokens):
        if_name = "%s.%s" % (self.interface_name(tokens[1]), tokens[3])
        yield self.defer(
            "fi.iface.%s" % self.interface_name(if_name),
            self.make_unit_inet_address,
            instance=deferable("instance"),
            interface=self.interface_name(if_name),
            unit=self.interface_name(if_name),
            address=self.to_prefix(tokens[7], None)
        )

    @match("routing-instances", ANY, "bridge-domains", ANY, "interface", ANY)
    def normalize_ri_bridge_interface(self, tokens):
        yield self.defer(
            "fi.iface.%s" % self.interface_name(tokens[5]),
            instance=tokens[1]
        )
        self.rebase(
            ("virtual-router", "default", "forwarding-instance", tokens[1], "interfaces",
             self.interface_name(tokens[5])),
            ("virtual-router", "default", "forwarding-instance", "default", "interfaces",
             self.interface_name(tokens[5]))
        )

    @match("routing-instances", ANY, "interface", ANY)
    def normalize_interface_routing_instances(self, tokens):
        yield self.defer(
            "fi.iface.%s" % self.interface_name(tokens[3]),
            instance=tokens[1]
        )

    @match("routing-instances", ANY, "route-distinguisher", ANY)
    def normalize_routing_instances_rd(self, tokens):
        yield self.make_forwarding_instance_rd(
            instance=tokens[1],
            rd=tokens[3]
        )

    @match("routing-instances", ANY, "instance-type", ANY)
    def make_routing_instances_type(self, tokens):
        yield self.make_forwarding_instance_type(
            instance=tokens[1],
            type=tokens[3]
        )

    @match("routing-instances", ANY, "vrf-target", ANY)
    def normalize_routing_instances_rt(self, tokens):
        yield self.make_forwarding_instance_export_target(
            instance=tokens[1],
            target=tokens[3][7:]
        )
        yield self.make_forwarding_instance_import_target(
            instance=tokens[1],
            target=tokens[3][7:]
        )

    @match("routing-instances", ANY, "vrf-target", "export", ANY)
    def normalize_routing_instances_rt_export(self, tokens):
        yield self.make_forwarding_instance_export_target(
            instance=tokens[1],
            target=tokens[4][7:]
        )

    @match("routing-instances", ANY, "vrf-target", "import", ANY)
    def normalize_routing_instances_rt_import(self, tokens):
        yield self.make_forwarding_instance_import_target(
            instance=tokens[1],
            target=tokens[4][7:]
        )
    """
    @match("routing-instances", ANY, "description", REST)
    def normalize_interface_routing_instances(self, tokens):
        yield self.make_forwarding_instance_description(
            instance=tokens[1],
            description=" ".join(tokens[3:])
        )
    """