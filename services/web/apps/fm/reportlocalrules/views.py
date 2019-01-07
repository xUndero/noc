# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Local Classification Rules Report
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.utils.html import escape
# NOC modules
from noc.lib.app.reportapplication import ReportApplication
from noc.fm.models.eventclassificationrule import EventClassificationRule
from noc.lib.text import indent
from noc.core.translation import ugettext as _
from noc.core.collection.base import Collection


class ReportClassificationRules(ReportApplication):
    title = _("Local Classification Rules (JSON)")

    def report_html(self, request, result=None, query=None):
        builtins = Collection.get_builtins("fm.eventclassificationrules")
        r = ["["]
        r += [",\n".join([
            indent(r.to_json())
            for r in EventClassificationRule.objects.order_by("name")
            if r.uuid and unicode(r.uuid) not in builtins
        ])]
        r += ["]", ""]
        return "<pre>" + escape("\n".join(r)) + "</pre>"
