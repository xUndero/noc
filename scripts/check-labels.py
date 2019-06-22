#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Check gitlab MR labels
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import print_function
import os
import sys


VAR_LABELS = "CI_MERGE_REQUEST_LABELS"
VAR_CI = "CI"
ERR_OK = 0
ERR_NO_LABELS = 1
ERR_MISSED = 2
ERR_MULTIPLE = 3
ERR_INVALID = 4

PRI_LABELS = ["pri::p1", "pri::p2", "pri::p3", "pri::p4"]
COMP_LABELS = ["comp::trivial", "comp::low", "comp::medium", "comp::high"]
KIND_LABELS = ["kind::feature", "kind::improvement", "kind::bug", "kind::cleanup"]


def die(code, msg, *args):
    print(msg % args)
    sys.exit(code)


def get_labels():
    if VAR_LABELS not in os.environ and VAR_CI not in os.environ:
        die(
            ERR_NO_LABELS,
            "%s environment variable is not defined. Must be called within Gitlab CI",
            VAR_LABELS
        )
    return os.environ.get(VAR_LABELS, "").split(",")


def go_url(anchor):
    return "https://docs.getnoc.com/master/en/go.html#%s" % anchor


def check_pri(labels):
    """
    Check `pri::*`
    :param labels:
    :return:
    """
    pri = [x for x in labels if x.startswith("pri::")]
    if not pri:
        die(
            ERR_MISSED,
            "pri::* label is not set. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(PRI_LABELS), go_url("dev-mr-labels-pri")
        )
    if len(pri) > 1:
        die(
            ERR_MULTIPLE,
            "Multiple pri::* labels defined. Must be exactly one.\n"
            "Refer to %s for details.",
            go_url("dev-mr-labels-priority")
        )
    pri = pri[0]
    if pri not in PRI_LABELS:
        die(
            ERR_INVALID,
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(PRI_LABELS), go_url("dev-mr-labels-pri")
        )


def check_comp(labels):
    """
    Check `comp::*`
    :param labels:
    :return:
    """
    comp = [x for x in labels if x.startswith("comp::")]
    if not comp:
        die(
            ERR_MISSED,
            "comp::* label is not set. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(COMP_LABELS), go_url("dev-mr-labels-comp")
        )
    if len(comp) > 1:
        die(
            ERR_MULTIPLE,
            "Multiple comp::* labels defined. Must be exactly one.\n"
            "Refer to %s for details.",
            go_url("dev-mr-labels-comp")
        )
    comp = comp[0]
    if comp not in COMP_LABELS:
        die(
            ERR_INVALID,
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(COMP_LABELS), go_url("dev-mr-labels-comp")
        )


def check_kind(labels):
    """
    Check `kind::*`
    :param labels:
    :return:
    """
    kind = [x for x in labels if x.startswith("kind::")]
    if not kind:
        die(
            ERR_MISSED,
            "kind::* label is not set. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(KIND_LABELS), go_url("dev-mr-labels-kind")
        )
    if len(kind) > 1:
        die(
            ERR_MULTIPLE,
            "Multiple kind::* labels defined. Must be exactly one.\n"
            "Refer to %s for details.",
            go_url("dev-mr-labels-kind")
        )
    kind = kind[0]
    if kind not in KIND_LABELS:
        die(
            ERR_INVALID,
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details.",
            ", ".join(KIND_LABELS), go_url("dev-mr-labels-kind")
        )


def check_affected(labels, name):
    n = sum(1 for x in labels if x == name)
    if not n:
        die(
            ERR_MISSED,
            "'%s' label is not set.\n"
            "Refer to %s for details.",
            name, go_url("dev-mr-labels-affected")
        )


def main():
    labels = get_labels()
    if "--pri" in sys.argv:
        check_pri(labels)
    if "--comp" in sys.argv:
        check_comp(labels)
    if "--kind" in sys.argv:
        check_kind(labels)
    for area in ["core", "documentation", "ui", "profiles", "migration", "tests"]:
        if "--%s" % area in sys.argv:
            check_affected(labels, area)


if __name__ == "__main__":
    main()
