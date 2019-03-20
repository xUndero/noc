# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Cisco.IOS.get_metrics
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
# NOC modules
from noc.lib.text import parse_kv
from noc.sa.profiles.Generic.get_metrics import Script as GetMetricsScript, metrics


class Script(GetMetricsScript):
    name = "Cisco.IOS.get_metrics"

    rx_ipsla_probe = re.compile(
        r"(?:IPSLA operation id:|Round Trip Time \(RTT\) for.+Index)\s+(\d+)",
        re.MULTILINE
    )

    rx_ipsla_latest_rtt = re.compile(
        r"Latest RTT:\s+(\d+)"
    )

    @metrics(
        ["SLA | JITTER", "SLA | UDP RTT"],
        has_capability="Cisco | IP | SLA | Probes",
        volatile=False,
        access="C"  # CLI version
    )
    def get_ip_sla_udp_jitter_metrics(self, metrics):
        """
        Returns collected ip sla metrics in form
        probe id -> {
            rtt: RTT in seconds
        }
        :return:
        """
        setup_metrics = {tuple(m.path): m.id for m in metrics if m.metric in {"SLA | JITTER", "SLA | UDP RTT"}}
        v = self.cli("show ip sla statistics")
        metric_map = {"ipsla operation id": "name",
                      "latest rtt": "rtt",
                      "source to destination jitter min/avg/max": "sd_jitter",
                      "destination to source jitter min/avg/max": "ds_jitter",
                      "number of rtt": "num_rtt"}
        r_v = self.rx_ipsla_probe.split(v)
        if len(r_v) < 3:
            return {}

        for probe_id, data in zip(r_v[1::2], r_v[2::2]):
            p = parse_kv(metric_map, data)
            if ("", str(probe_id)) not in setup_metrics:
                continue
            if "rtt" in p:
                # Latest RTT: 697 milliseconds
                rtt = p["rtt"].split()[0]
                try:
                    self.set_metric(id=("SLA | UDP RTT", ("", probe_id)),
                                    metric="SLA | UDP RTT",
                                    value=float(rtt) * 1000,
                                    multi=True)

                except ValueError:
                    pass
            if "sd_jitter" in p:
                # Source to Destination Jitter Min/Avg/Max: 0/8/106 milliseconds
                jitter = p["sd_jitter"].split()[0].split("/")[1]
                self.set_metric(id=("SLA | JITTER", ("", probe_id)),
                                metric="SLA | JITTER",
                                value=float(jitter) * 1000,
                                multi=True)

    @metrics(
        ["SLA | ICMP RTT"],
        has_capability="Cisco | IP | SLA | Probes",
        volatile=False,
        access="C"  # CLI version
    )
    def get_ip_sla_icmp_echometrics(self, metrics):
        """
        Returns collected ip sla metrics in form
        probe id -> {
            rtt: RTT in seconds
        }
        :return:
        """
        setup_metrics = {tuple(m.path): m.id for m in metrics if m.metric == "SLA | ICMP RTT" and
                         m.sla_type == "icmp-echo"}
        if not setup_metrics:
            self.logger.info("No icmp-echo sla probes.")
            return
        v = self.cli("show ip sla statistics")
        metric_map = {"ipsla operation id": "name",
                      "latest rtt": "rtt",
                      "number of rtt": "num_rtt"}

        r_v = self.rx_ipsla_probe.split(v)
        if len(r_v) < 3:
            return

        for probe_id, data in zip(r_v[1::2], r_v[2::2]):
            p = parse_kv(metric_map, data)
            if ("", str(probe_id)) not in setup_metrics:
                continue
            if "rtt" in p:
                # Latest RTT: 697 milliseconds
                rtt = p["rtt"].split()[0]
                try:
                    self.set_metric(id=setup_metrics[("", str(probe_id))],
                                    metric="SLA | ICMP RTT",
                                    path=("", probe_id),
                                    value=float(rtt) * 1000,
                                    multi=True)
                except ValueError:
                    pass
