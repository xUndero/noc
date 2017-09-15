# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# EventClassificationRule test
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
# Third-party modules
import pytest
# NOC modules
from noc.tests.util.jsonloader import json_loader
from noc.services.classifier.ruleset import RuleSet
from noc.fm.models.mib import MIB
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.profile import Profile
from noc.fm.models.eventclass import EventClass
from noc.fm.models.activeevent import ActiveEvent
from noc.config import config


COLLECTION_NAME = "test.events"
DEFAULT_EVENT_CLASS = "Unknown | Default"
DEFAULT_PROFILE = "Generic.Host"
MO_ADDRESS = "127.0.0.1"
MO_NAME = "test"
MO_ID = 1


@pytest.fixture(scope="module")
def ruleset():
    ruleset = RuleSet()
    ruleset.load()
    return ruleset


@pytest.fixture(params=json_loader(config.tests.events_path))
def event(request):
    path, cfg = request.param
    coll = cfg.get("$collection", COLLECTION_NAME)
    assert coll == COLLECTION_NAME, "Invalid collection %s" % coll
    ec = EventClass.get_by_name(
        cfg.get("eventclass__name", DEFAULT_EVENT_CLASS)
    )
    mo = ManagedObject(
        id=MO_ID,
        name=MO_NAME,
        address=MO_ADDRESS,
        profile=Profile.get_by_name(cfg.get("profile__name", DEFAULT_PROFILE))
    )
    now = datetime.datetime.now()
    data = cfg.get("data", {})
    source = data.pop("source", "other")
    event = ActiveEvent(
        timestamp=now,
        start_timestamp=now,
        managed_object=mo,
        source=source,
        raw_vars=data,
        repeats=1
    )
    request.fixturename = "events-%s" % cfg.get("uuid")
    # request.fspath = path
    return event, ec, cfg.get("vars", {})


def test_event(ruleset, event):
    e, expected_class, expected_vars = event
    e_vars = e.raw_vars.copy()
    if e.source == "SNMP Trap":
        e_vars.update(MIB.resolve_vars(e.raw_vars))
    rule, r_vars = ruleset.find_rule(e, e_vars)
    assert rule is not None, "Cannot find matching rule"
    assert rule.event_class == expected_class, "Mismatched event class %s vs %s" % (
        rule.event_class.name, expected_class.name)
    ruleset.eval_vars(event, rule.event_class, e_vars)
    assert e_vars == expected_vars, "Mismatched vars"
