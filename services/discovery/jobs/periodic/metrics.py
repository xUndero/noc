# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Metric collector
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from threading import Lock
import operator
from collections import namedtuple
import itertools
import time
from collections import defaultdict

# Third-party modules
import six
import cachetools
from pymongo import ReadPreference

# NOC modules
from noc.services.discovery.jobs.base import DiscoveryCheck
from noc.sa.models.managedobjectprofile import ManagedObjectProfile
from noc.inv.models.interfaceprofile import InterfaceProfile
from noc.inv.models.interface import Interface
from noc.inv.models.subinterface import SubInterface
from noc.fm.models.alarmclass import AlarmClass
from noc.pm.models.metrictype import MetricType
from noc.sla.models.slaprofile import SLAProfile
from noc.sla.models.slaprobe import SLAProbe
from noc.pm.models.thresholdprofile import ThresholdProfile
from noc.core.handler import get_handler
from noc.core.hash import hash_str


MAX31 = 0x7FFFFFFF
MAX32 = 0xFFFFFFFF
MAX64 = 0xFFFFFFFFFFFFFFFF

NS = 1000000000.0

MT_COUNTER = "counter"
MT_BOOL = "bool"
MT_DELTA = "delta"
MT_COUNTER_DELTA = {MT_COUNTER, MT_DELTA}

WT_MEASURES = "m"
WT_TIME = "t"

SCOPE_OBJECT = "object"
SCOPE_INTERFACE = "interface"
SCOPE_SLA = "sla"

metrics_lock = Lock()

MetricConfig = namedtuple(
    "MetricConfig",
    ["metric_type", "enable_box", "enable_periodic", "is_stored", "threshold_profile"],
)


class MData(object):
    __slots__ = ("id", "ts", "metric", "path", "value", "scale", "type", "abs_value", "label")

    def __init__(
        self, id, ts, metric, path=None, value=None, scale=None, type=None, abs_value=None
    ):
        self.id = id
        self.ts = ts
        self.metric = metric
        self.path = path
        self.value = value
        self.scale = scale
        self.type = type
        self.abs_value = abs_value
        if path:
            self.label = "%s|%s" % (metric, "|".join(str(p) for p in path))
        else:
            self.label = metric

    def __repr__(self):
        return "<MData #%s %s>" % (self.id, self.metric)


class MetricsCheck(DiscoveryCheck):
    """
    MAC discovery
    """

    name = "metrics"
    required_script = "get_metrics"

    _object_profile_metrics = cachetools.TTLCache(1000, 60)
    _interface_profile_metrics = cachetools.TTLCache(1000, 60)
    _slaprofile_metrics = cachetools.TTLCache(1000, 60)

    S_OK = 0
    S_WARN = 1
    S_ERROR = 2

    SMAP = {0: "ok", 1: "warn", 2: "error"}

    SEV_MAP = {1: 2000, 2: 3000}

    SLA_CAPS = ["Cisco | IP | SLA | Probes"]

    def __init__(self, *args, **kwargs):
        super(MetricsCheck, self).__init__(*args, **kwargs)
        self.id_count = itertools.count()
        self.id_metrics = {}

    @staticmethod
    @cachetools.cached({})
    def get_ac_pm_thresholds():
        return AlarmClass.get_by_name("NOC | PM | Out of Thresholds")

    @classmethod
    @cachetools.cachedmethod(
        operator.attrgetter("_object_profile_metrics"), lock=lambda _: metrics_lock
    )
    def get_object_profile_metrics(cls, p_id):
        r = {}
        opr = ManagedObjectProfile.get_by_id(id=p_id)
        if not opr:
            return r
        for m in opr.metrics:
            mt_id = m.get("metric_type")
            if not mt_id:
                continue
            mt = MetricType.get_by_id(mt_id)
            if not mt:
                continue
            if m.get("threshold_profile"):
                threshold_profile = ThresholdProfile.get_by_id(m.get("threshold_profile"))
            else:
                threshold_profile = None
            r[mt.name] = MetricConfig(
                mt,
                m.get("enable_box", True),
                m.get("enable_periodic", True),
                m.get("is_stored", True),
                threshold_profile,
            )
        return r

    @staticmethod
    def quote_path(path):
        """
        Convert path list to ClickHouse format
        :param path:
        :return:
        """
        return "[%s]" % ",".join("'%s'" % p for p in path)

    @staticmethod
    def config_from_settings(m):
        """
        Returns MetricConfig from .metrics field
        :param m:
        :return:
        """
        return MetricConfig(
            m.metric_type, m.enable_box, m.enable_periodic, m.is_stored, m.threshold_profile
        )

    @classmethod
    @cachetools.cachedmethod(
        operator.attrgetter("_interface_profile_metrics"), lock=lambda _: metrics_lock
    )
    def get_interface_profile_metrics(cls, p_id):
        r = {}
        ipr = InterfaceProfile.get_by_id(id=p_id)
        if not ipr:
            return r
        for m in ipr.metrics:
            r[m.metric_type.name] = cls.config_from_settings(m)
        return r

    @classmethod
    @cachetools.cachedmethod(
        operator.attrgetter("_slaprofile_metrics"), lock=lambda _: metrics_lock
    )
    def get_slaprofile_metrics(cls, p_id):
        r = {}
        spr = SLAProfile.get_by_id(p_id)
        if not spr:
            return r
        for m in spr.metrics:
            r[m.metric_type.name] = cls.config_from_settings(m)
        return r

    def get_object_metrics(self):
        """
        Populate metrics list with objects metrics
        :return:
        """
        metrics = []
        o_metrics = self.get_object_profile_metrics(self.object.object_profile.id)
        self.logger.debug("Object metrics: %s", o_metrics)
        for metric in o_metrics:
            if (self.is_box and not o_metrics[metric].enable_box) or (
                self.is_periodic and not o_metrics[metric].enable_periodic
            ):
                continue
            m_id = next(self.id_count)
            metrics += [{"id": m_id, "metric": metric}]
            self.id_metrics[m_id] = o_metrics[metric]
        if not metrics:
            self.logger.info("Object metrics are not configured. Skipping")
        return metrics

    def get_subinterfaces(self):
        subs = defaultdict(list)  # interface id -> [{"name":, "ifindex":}]
        for si in (
            SubInterface._get_collection()
            .with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
            .find({"managed_object": self.object.id}, {"name": 1, "interface": 1, "ifindex": 1})
        ):
            subs[si["interface"]] += [{"name": si["name"], "ifindex": si.get("ifindex")}]
        return subs

    def get_interface_metrics(self):
        """
        Populate metrics list with interface metrics
        :return:
        """
        subs = None
        metrics = []
        for i in (
            Interface._get_collection()
            .with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
            .find(
                {"managed_object": self.object.id, "type": "physical"},
                {"_id": 1, "name": 1, "ifindex": 1, "profile": 1},
            )
        ):
            ipr = self.get_interface_profile_metrics(i["profile"])
            self.logger.debug("Interface %s. ipr=%s", i["name"], ipr)
            if not ipr:
                continue  # No metrics configured
            i_profile = InterfaceProfile.get_by_id(i["profile"])
            if i_profile.allow_subinterface_metrics and subs is None:
                # Resolve subinterfaces
                subs = self.get_subinterfaces()
            ifindex = i.get("ifindex")
            for metric in ipr:
                if (self.is_box and not ipr[metric].enable_box) or (
                    self.is_periodic and not ipr[metric].enable_periodic
                ):
                    continue
                m_id = next(self.id_count)
                m = {"id": m_id, "metric": metric, "path": ["", "", "", i["name"]]}
                if ifindex is not None:
                    m["ifindex"] = ifindex
                metrics += [m]
                self.id_metrics[m_id] = ipr[metric]
                if i_profile.allow_subinterface_metrics:
                    for si in subs[i["_id"]]:
                        m_id = next(self.id_count)
                        m = {
                            "id": m_id,
                            "metric": metric,
                            "path": ["", "", "", i["name"], si["name"]],
                        }
                        if si["ifindex"] is not None:
                            m["ifindex"] = si["ifindex"]
                        metrics += [m]
                        self.id_metrics[m_id] = ipr[metric]
        if not metrics:
            self.logger.info("Interface metrics are not configured. Skipping")
        return metrics

    def get_sla_metrics(self):
        if not self.has_any_capability(self.SLA_CAPS):
            self.logger.info("SLA not configured, skipping SLA metrics")
        metrics = []
        for p in (
            SLAProbe._get_collection()
            .with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
            .find(
                {"managed_object": self.object.id}, {"name": 1, "group": 1, "profile": 1, "type": 1}
            )
        ):
            if not p.get("profile"):
                self.logger.debug("Probe %s has no profile. Skipping", p["name"])
                continue
            pm = self.get_slaprofile_metrics(p["profile"])
            if not pm:
                self.logger.debug(
                    "Probe %s has profile '%s' with no configured metrics. " "Skipping",
                    p["name"],
                    p.profile.name,
                )
                continue
            for metric in pm:
                if (self.is_box and not pm[metric].enable_box) or (
                    self.is_periodic and not pm[metric].enable_periodic
                ):
                    continue
                m_id = next(self.id_count)
                metrics += [
                    {
                        "id": m_id,
                        "metric": metric,
                        "path": [p.get("group", ""), p["name"]],
                        "sla_type": p["type"],
                    }
                ]
                self.id_metrics[m_id] = pm[metric]
        if not metrics:
            self.logger.info("SLA metrics are not configured. Skipping")
        return metrics

    def process_result(self, result):
        """
        Process IGetMetrics result
        :param result:
        :return:
        """
        # Restore last counter state
        if self.has_artefact("reboot"):
            self.logger.info("Resetting counter context due to detected reboot")
            self.job.context["counters"] = {}
        counters = self.job.context["counters"]
        alarms = []
        events = []
        data = defaultdict(dict)  # table -> item hash -> {field:value, ...}
        n_metrics = 0
        mo_id = self.object.bi_id
        ts_cache = {}  # timestamp -> (date, ts)
        # Calculate time_delta
        time_delta = self.job.context.get("time_delta", None)
        if time_delta:
            del self.job.context["time_delta"]  # Remove from context
        if time_delta and time_delta > 0xFFFF:
            self.logger.info(
                "time_delta overflow (%d). time_delta measurement will be dropped" % time_delta
            )
            time_delta = None
        # Process collected metrics
        for m in result:
            path = m.path
            cfg = self.id_metrics.get(m.id)
            if m.type in MT_COUNTER_DELTA:
                # Counter type
                if path:
                    key = "%x|%s" % (cfg.metric_type.bi_id, "|".join(str(p) for p in path))
                else:
                    key = "%x" % cfg.metric_type.bi_id
                # Restore old value and save new
                r = counters.get(key)
                counters[key] = (m.ts, m.value)
                if r is None:
                    # No stored state
                    self.logger.debug(
                        "[%s] COUNTER value is not found. " "Storing and waiting for a new result",
                        m.label,
                    )
                    continue
                # Calculate counter
                self.logger.debug(
                    "[%s] Old value: %s@%s, new value: %s@%s.", m.label, r[1], r[0], m.value, m.ts
                )
                if m.type == MT_COUNTER:
                    cv = self.convert_counter(m, r)
                else:
                    cv = self.convert_delta(m, r)
                if cv is None:
                    # Counter stepback or other errors
                    # Remove broken value
                    self.logger.debug(
                        "[%s] Counter stepback from %s@%s to %s@%s: Skipping",
                        m.label,
                        r[1],
                        r[0],
                        m.value,
                        m.ts,
                    )
                    del counters[key]
                    continue
                m.value = cv
                m.abs_value = cv * m.scale
            elif m.type == MT_BOOL:
                # Convert boolean type
                m.abs_value = 1 if m.value else 0
            else:
                # Gauge
                m.abs_value = m.value * m.scale

            self.logger.debug(
                "[%s] Measured value: %s. Scale: %s. Resulting value: %s",
                m.label,
                m.value,
                m.scale,
                m.abs_value,
            )
            # Schedule to store
            if cfg.is_stored:
                tsc = ts_cache.get(m.ts)
                if not tsc:
                    lt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(m.ts // 1000000000))
                    tsc = (lt.split(" ")[0], lt)
                    ts_cache[m.ts] = tsc
                if path:
                    item_hash = hash_str(str((tsc[1], mo_id, path)))
                else:
                    item_hash = hash_str(str((tsc[1], mo_id)))
                record = data[cfg.metric_type.scope.table_name].get(item_hash)
                if not record:
                    record = {"date": tsc[0], "ts": tsc[1], "managed_object": mo_id}
                    if path:
                        record["path"] = path
                    data[cfg.metric_type.scope.table_name][item_hash] = record
                field = cfg.metric_type.field_name
                try:
                    record[field] = cfg.metric_type.clean_value(m.abs_value)
                except ValueError as e:
                    self.logger.info("[%s] Cannot clean value %s: %s", m.label, m.abs_value, e)
                    continue
                # Attach time_delta, when required
                if time_delta and cfg.metric_type.scope.enable_timedelta:
                    data[cfg.metric_type.scope.table_name][item_hash]["time_delta"] = time_delta
                n_metrics += 1
            if cfg.threshold_profile and m.abs_value is not None:
                alarm, event = self.process_thresholds(m, cfg)
                alarms += alarm
                events += event
        return n_metrics, data, alarms, events

    def handler(self):
        self.logger.info("Collecting metrics")
        # Build get_metrics input parameters
        metrics = self.get_object_metrics()
        metrics += self.get_interface_metrics()
        metrics += self.get_sla_metrics()
        if not metrics:
            self.logger.info("No metrics configured. Skipping")
            return
        # Collect metrics
        ts = time.time()
        if "last_run" in self.job.context and self.job.context["last_run"] < ts:
            self.job.context["time_delta"] = int(round(ts - self.job.context["last_run"]))
        self.job.context["last_run"] = ts
        self.logger.debug("Collecting metrics: %s", metrics)
        result = [MData(**r) for r in self.object.scripts.get_metrics(metrics=metrics)]
        if not result:
            self.logger.info("No metrics found")
            return
        # Process results
        n_metrics, data, alarms, events = self.process_result(result)
        # Send metrics
        if n_metrics:
            self.logger.info("Spooling %d metrics", n_metrics)
            for table in data:
                self.service.register_metrics(table, list(six.itervalues(data[table])))
        # Set up threshold alarms
        self.logger.info("%d alarms detected", len(alarms))
        if events:
            self.logger.info("%d events detected", len(events))
        self.job.update_umbrella(self.get_ac_pm_thresholds(), alarms)

    def convert_delta(self, m, r):
        """
        Calculate value from delta, gently handling overflows
        :param m: MData
        :param r: Old state (ts, value)
        """
        if m.value < r[1]:
            # Counter decreased, either due wrap or stepback
            if r[1] <= MAX31:
                mc = MAX31
            elif r[1] <= MAX32:
                mc = MAX32
            else:
                mc = MAX64
            # Direct distance
            d_direct = r[1] - m.value
            # Wrap distance
            d_wrap = m.value + (mc - r[1])
            if d_direct < d_wrap:
                # Possible counter stepback
                # Skip value
                self.logger.debug("[%s] Counter stepback: %s -> %s", m.label, r[1], m.value)
                return None
            else:
                # Counter wrap
                self.logger.debug("[%s] Counter wrap: %s -> %s", m.label, r[1], m.value)
                return d_wrap
        else:
            return m.value - r[1]

    def convert_counter(self, m, r):
        """
        Calculate value from counter, gently handling overflows
        :param m: MData
        :param r: Old state (ts, value)
        """
        dt = (float(m.ts) - float(r[0])) / NS
        delta = self.convert_delta(m, r)
        if delta is None:
            return delta
        return float(delta) / dt

    def get_window_function(self, m, cfg):
        """
        Check thresholds
        :param m: dict with metric result
        :param cfg: MetricConfig
        :return: Value or None
        """
        # Build window state key
        if m.path:
            key = "%x|%s" % (cfg.metric_type.bi_id, "|".join(str(p) for p in m.path))
        else:
            key = "%x" % cfg.metric_type.bi_id
        #
        states = self.job.context["metric_windows"]
        value = m.abs_value
        ts = m.ts // 1000000000
        # Do not store single-value windows
        window_type = cfg.threshold_profile.window_type
        ws = cfg.threshold_profile.window
        drop_window = window_type == "m" and ws == 1
        # Restore window
        if drop_window:
            window = [(ts, value)]
            window_full = True
            if key in states:
                del states[key]
        else:
            window = states.get(key, [])
            window += [(ts, value)]
            # Trim window according to policy
            if window_type == WT_MEASURES:
                # Leave fixed amount of measures
                window = window[-ws:]
                window_full = len(window) == ws
            elif window_type == WT_TIME:
                # Time-based window
                window_full = ts - window[0][0] >= ws
                while ts - window[0][0] > ws:
                    window.pop(0)
            else:
                self.logger.error(
                    "Cannot calculate thresholds for %s (%s): Invalid window type '%s'",
                    m.metric,
                    m.path,
                    window_type,
                )
                return None
            # Store back to context
            states[key] = window
        if not window_full:
            self.logger.error(
                "Cannot calculate thresholds for %s (%s): Window is not filled", m.metric, m.path
            )
            return None
        # Process window function
        wf = cfg.threshold_profile.get_window_function()
        if not wf:
            self.logger.error(
                "Cannot calculate thresholds for %s (%s): Invalid window function %s",
                m.metric,
                m.path,
                cfg.threshold_profile.window_function,
            )
            return None
        try:
            return wf(window, cfg.threshold_profile.window_config)
        except ValueError as e:
            self.logger.error("Cannot calculate thresholds for %s (%s): %s", m.metric, m.path, e)
            return None

    def process_thresholds(self, m, cfg):
        """
        Check thresholds
        :param m: dict with metric result
        :param cfg: MetricConfig
        :return: List of umbrella alarm details
        """
        alarms = []
        events = []
        new_threshold = None
        # Check if profile has configured thresholds
        if not cfg.threshold_profile.thresholds:
            return alarms
        w_value = self.get_window_function(m, cfg)
        if w_value is None:
            return alarms, events
        # Metrics path
        path = m.metric
        if m.path:
            path = "%s | %s" % (path, " | ".join(m.path))
        # Get active threshold name
        active = self.job.context["active_thresholds"].get(path)
        if active:
            # Check we should close existing threshold
            for th in cfg.threshold_profile.thresholds:
                if th.is_open_match(w_value):
                    new_threshold = th
                    break
            threshold = cfg.threshold_profile.find_threshold(active)
            if new_threshold and threshold != new_threshold:
                # Close Event
                active = None  # Reset threshold
                del self.job.context["active_thresholds"][path]
                if threshold.close_event_class:
                    events += self.get_event_cfg(
                        cfg, threshold.name, threshold.close_event_class.name, path, w_value
                    )
                if threshold.close_handler:
                    if threshold.close_handler.allow_threshold:
                        handler = threshold.close_handler.get_handler()
                        if handler:
                            try:
                                handler(self, cfg, threshold, w_value)
                            except Exception as e:
                                self.logger.error("Exception when calling close handler: %s", e)
                    else:
                        self.logger.warning("Handler is not allowed for Thresholds")
                elif threshold.alarm_class:
                    # Remain umbrella alarm
                    alarms += self.get_umbrella_alarm_cfg(cfg, threshold, path, w_value)
            elif threshold:
                if threshold.is_clear_match(w_value):
                    # Close Event
                    active = None  # Reset threshold
                    del self.job.context["active_thresholds"][path]
                    if threshold.close_event_class:
                        events += self.get_event_cfg(
                            cfg, threshold.name, threshold.close_event_class.name, path, w_value
                        )
                    if threshold.close_handler:
                        if threshold.close_handler.allow_threshold:
                            handler = threshold.close_handler.get_handler()
                            if handler:
                                try:
                                    handler(self, cfg, threshold, w_value)
                                except Exception as e:
                                    self.logger.error("Exception when calling close handler: %s", e)
                        else:
                            self.logger.warning("Handler is not allowed for Thresholds")
                elif threshold.alarm_class:
                    # Remain umbrella alarm
                    alarms += self.get_umbrella_alarm_cfg(cfg, threshold, path, w_value)
            else:
                # Threshold has been reconfigured or deleted
                active = None
                del self.job.context["active_thresholds"][path]
        if not active:
            # Check opening thresholds only if no active threshold remains
            for threshold in cfg.threshold_profile.thresholds:
                if not threshold.is_open_match(w_value):
                    continue
                # Set context
                self.job.context["active_thresholds"][path] = threshold.name
                if threshold.open_event_class:
                    # Raise Event
                    events += self.get_event_cfg(
                        cfg, threshold.name, threshold.open_event_class.name, path, w_value
                    )
                if threshold.open_handler:
                    if threshold.open_handler.allow_threshold:
                        # Call handler
                        handler = threshold.open_handler.get_handler()
                        if handler:
                            try:
                                handler(self, cfg, threshold, w_value)
                            except Exception as e:
                                self.logger.error("Exception when calling open handler: %s", e)
                    else:
                        self.logger.warning("Handler is not allowed for Thresholds")
                if threshold.alarm_class:
                    # Raise umbrella alarm
                    alarms += self.get_umbrella_alarm_cfg(cfg, threshold, path, w_value)
                break
        return alarms, events

    def get_umbrella_alarm_cfg(self, metric_config, threshold, path, value):
        """
        Get configuration for umbrella alarm
        :param threshold_profile:
        :param threshold:
        :param metric_config:
        :param value:
        :return: List of dicts or empty list
        """
        alarm_cfg = {
            "alarm_class": threshold.alarm_class,
            "path": path,
            "severity": threshold.alarm_class.default_severity.severity,
            "vars": {
                "path": path,
                "metric": metric_config.metric_type.name,
                "value": value,
                "window_type": metric_config.threshold_profile.window_type,
                "window": metric_config.threshold_profile.window,
                "window_function": metric_config.threshold_profile.window_function,
            },
        }
        if metric_config.threshold_profile.umbrella_filter_handler:
            try:
                handler = get_handler(metric_config.threshold_profile.umbrella_filter_handler)
                if handler:
                    alarm_cfg = handler(self, alarm_cfg)
                    if not alarm_cfg:
                        return []
            except Exception as e:
                self.logger.error("Exception when loading handler %s", e)
        return [alarm_cfg]

    def get_event_cfg(self, metric_config, threshold, event_class, path, value):
        """
        Get configuration for umbrella alarm
        :param metric_config:
        :param threshold:
        :param event_class:
        :param path:
        :param value:
        :return: List of dicts or empty list
        """
        full_path = path
        if path != metric_config.metric_type.name:
            path = path.replace("%s |" % metric_config.metric_type.name, "")
        result = False
        raw_vars = {
            "path": path.strip(),
            "full_path": full_path,
            "threshold": threshold,
            "metric": metric_config.metric_type.name,
            "value": str(value),
            "window_type": metric_config.threshold_profile.window_type,
            "window": str(metric_config.threshold_profile.window),
            "window_function": metric_config.threshold_profile.window_function,
        }
        if metric_config.threshold_profile.umbrella_filter_handler:
            try:
                handler = get_handler(metric_config.threshold_profile.umbrella_filter_handler)
                if handler:
                    raw_vars = handler(self, raw_vars)
                    if not raw_vars:
                        return []
            except Exception as e:
                self.logger.error("Exception when loading handler %s", e)
        try:
            self.raise_event(event_class, raw_vars)
            result = True
        except Exception as e:
            self.logger.error("Exception when send message %s", e)
        if result:
            return [raw_vars]

    def raise_event(self, event_class, raw_vars=None):
        if not raw_vars:
            raw_vars = {}
        data = {"$event": {"class": event_class, "vars": raw_vars}}
        msg = {"ts": time.time(), "object": self.object.id, "data": data}
        self.logger.info("Pub Event: %s", msg)
        self.job.service.pub("events.%s" % self.object.pool.name, msg)
