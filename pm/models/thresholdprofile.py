# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ThresholdProfile model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import operator
from threading import Lock

# Third-party modules
import six
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, ListField, EmbeddedDocumentField, FloatField
import cachetools

# NOC modules
from noc.main.models.template import Template
from noc.main.models.handler import Handler
from noc.fm.models.alarmclass import AlarmClass
from noc.fm.models.eventclass import EventClass
from noc.core.window import wf_choices
from noc.core.mongo.fields import PlainReferenceField, ForeignKeyField
from noc.core.window import get_window_function


id_lock = Lock()


@six.python_2_unicode_compatible
class ThresholdConfig(EmbeddedDocument):
    # Open condition
    op = StringField(choices=["<", "<=", ">=", ">"])
    value = FloatField()
    # Closing condition
    clear_op = StringField(choices=["<", "<=", ">=", ">"])
    clear_value = FloatField()
    # Umbrella alarm class
    alarm_class = PlainReferenceField(AlarmClass)
    # Send event to correlator
    open_event_class = PlainReferenceField(EventClass)
    close_event_class = PlainReferenceField(EventClass)
    # Handlers to call on open and close thresholds
    open_handler = PlainReferenceField(Handler)
    close_handler = PlainReferenceField(Handler)
    #
    template = ForeignKeyField(Template)

    def __str__(self):
        return "%s %s %s %s" % (self.op, self.value, self.clear_op, self.clear_value)

    def is_open_match(self, value):
        """
        Check if threshold profile is matched for open condition
        :param value:
        :return:
        """
        return (
            (self.op == "<" and value < self.value)
            or (self.op == "<=" and value <= self.value)
            or (self.op == ">=" and value >= self.value)
            or (self.op == ">" and value > self.value)
        )

    def is_clear_match(self, value):
        """
        Check if threshold profile is matched for clear condition
        :param value:
        :return:
        """
        return (
            (self.clear_op == "<" and value < self.clear_value)
            or (self.clear_op == "<=" and value <= self.clear_value)
            or (self.clear_op == ">=" and value >= self.clear_value)
            or (self.clear_op == ">" and value > self.clear_value)
        )

    @property
    def name(self):
        return "%s %s %s %s" % (self.op, self.value, self.clear_op, self.clear_value)


# @todo: on_delete_check
@six.python_2_unicode_compatible
class ThresholdProfile(Document):
    meta = {"collection": "thresholdprofiles", "strict": False, "auto_create_index": False}

    name = StringField(unique=True)
    description = StringField()
    # Handler to filter and modify umbrella alarms
    umbrella_filter_handler = StringField()
    # Window function settings
    # Window depth
    window_type = StringField(max_length=1, choices=[("m", "Measurements"), ("t", "Time")])
    # Window size. Depends on window type
    # * m - amount of measurements
    # * t - time in seconds
    window = IntField(default=1)
    # Window function
    # Accepts window as a list of [(timestamp, value)]
    # and window_config
    # and returns float value
    window_function = StringField(choices=wf_choices, default="last")
    # Window function configuration
    window_config = StringField()
    # thresholds config
    thresholds = ListField(EmbeddedDocumentField(ThresholdConfig))

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return ThresholdProfile.objects.filter(id=id).first()

    def get_window_function(self):
        """
        Returns window funciton or None if invalid name given
        :returns: Callable or None
        """
        return get_window_function(self.window_function)

    def find_threshold(self, name):
        """
        Find Threshold Config by name
        :param name: Threshold name
        :return: ThresholdConfig or None
        """
        for cfg in self.thresholds:
            if cfg.name == name:
                return cfg
        return None
