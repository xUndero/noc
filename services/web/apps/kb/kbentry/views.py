# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# kb.kbentry application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2012 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from django.http import HttpResponse
import mimetypes
# NOC modules
from noc.lib.app.extmodelapplication import ExtModelApplication, view
from noc.kb.models.kbentry import KBEntry
from noc.kb.models.kbentryhistory import KBEntryHistory
from noc.kb.models.kbentryattachment import KBEntryAttachment
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
        # del r["body"]
        return r

    @view(r"^(?P<id>\d+)/history/$", access="read", api=True)
    def api_get_entry_history(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        return {"data": [{"timestamp": self.to_json(h.timestamp), "user": str(h.user), "diff": h.diff} for h in
                         KBEntryHistory.objects.filter(kb_entry=o).order_by("-timestamp")]}

    @view(r"^(?P<id>\d+)/html/$", access="read", api=True)
    def api_get_entry_html(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        return self.render_plain_text(o.html)

    @view(r"^most_popular/$", access="read", api=True)
    def api_get_most_popular(self, request):
        return KBEntry.most_popular()

    @view(r"^(?P<id>\d+)/attachments/$", access="read", api=True, method=["GET"])
    def api_post_set_attachments(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        return [{"name": x.name, "size": x.size, "mtime": self.to_json(x.mtime), "description": x.description}
                for x in KBEntryAttachment.objects.filter(kb_entry=o, is_hidden=False).order_by("name")]

    @view(r"^(?P<id>\d+)/attachment/(?P<name>.+)/$", access="read", api=True, method=["GET"])
    def api_get_attachment(self, request, id, name):
        o = self.get_object_or_404(KBEntry, id=id)
        attach = self.get_object_or_404(KBEntryAttachment, kb_entry=o, name=name)
        file_mime = mimetypes.guess_type(attach.file.name)
        response = HttpResponse(attach.file, content_type=file_mime or "application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=\"%s\"" % attach.file.name
        return response

    @view(r"^(?P<id>\d+)/attachment/(?P<name>.+)/$", access="read", api=True, method=["DELETE"])
    def api_delete_attachment(self, request, id, name):
        o = self.get_object_or_404(KBEntry, id=id)
        attach = self.get_object_or_404(KBEntryAttachment, kb_entry=o, name=name)
        attach.delete()
        return self.response({"result": "Delete succesful"}, status=self.OK)

    @view(r"^(?P<id>\d+)/attach/$", access="write", api=True, method=["POST"])
    def api_post_set_attachment(self, request, id):
        o = self.get_object_or_404(KBEntry, id=id)
        attach = KBEntryAttachment(kb_entry=o, name="uploaded_file1", description="", file=request.FILES["file"])
        attach.save()
        return self.response({"result": "Upload succesful"}, status=self.OK)
