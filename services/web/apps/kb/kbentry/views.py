# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# kb.kbentry application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2012 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.app.extmodelapplication import ExtModelApplication, view
from noc.kb.models.kbentry import KBEntry
from noc.kb.models.kbentryhistory import KBEntryHistory
from noc.core.translation import ugettext as _


class KBEntryApplication(ExtModelApplication):
    """
    AdministrativeDomain application
    """
    title = _("Entries")
    menu = [_("Setup"), _("Entries")]
    model = KBEntry

    def instance_to_dict(self, o, fields=None):
        r = super(KBEntryApplication, self).instance_to_dict(o, fields=fields)
        del r["body"]
        return r

    @view(r"^(?P<id>\d+)/history/$", access="read", api=True)
    def api_get_entry_history(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        return {"data": [{"timestamp": self.to_json(h.timestamp), "user": str(h.user)} for h in
                         KBEntryHistory.objects.filter(kb_entry=o).order_by("-timestamp")]}

    @view(r"^(?P<id>\d+)/html/$", access="read", api=True)
    def api_get_entry_html(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        return self.render_plain_text(o.html)

    @view(r"^most_popular/$", access="read", api=True)
    def api_get_most_popular(self, request):
        return KBEntry.most_popular()
