# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Parallel command execution
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.app.extapplication import ExtApplication
from noc.lib.app.application import view
from noc.core.translation import ugettext as _
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.commandsnippet import CommandSnippet
from noc.sa.models.action import Action
from noc.sa.interfaces.base import ListOfParameter, ModelParameter, DictParameter


class RunCommandsApplication(ExtApplication):
    title = _("Run Commands")
    menu = [_("Run Commands")]

    implied_permissions = {"launch": ["sa:objectlist:read"]}

    @view(url="^form/snippet/(?P<snippet_id>\d+)/$", method=["GET"], access="launch", api=True)
    def api_form_snippet(self, request, snippet_id):
        snippet = self.get_object_or_404(CommandSnippet, id=int(snippet_id))
        r = []
        vars = snippet.vars
        for k in vars:
            cfg = {"name": k, "fieldLabel": k, "allowBlank": not vars[k].get("required", False)}
            t = vars[k].get("type")
            if t == "int":
                cfg["xtype"] = "numberfield"
            else:
                cfg["xtype"] = "textfield"
            r += [cfg]
        return r

    @view(
        url="^form/action/(?P<action_id>[0-9a-f]{24})/$", method=["GET"], access="launch", api=True
    )
    def api_form_action(self, request, action_id):
        action = self.get_object_or_404(Action, id=action_id)
        r = []
        for p in action.params:
            cfg = {
                "name": p.name,
                "fieldLabel": p.description or p.name,
                "allowBlank": not p.is_required,
            }
            if p.type == "int":
                cfg["xtype"] = "numberfield"
            else:
                cfg["xtype"] = "textfield"
            r += [cfg]
        return r

    @view(
        url="^render/snippet/(?P<snippet_id>\d+)/$",
        method=["POST"],
        validate={
            "objects": ListOfParameter(element=ModelParameter(ManagedObject)),
            "config": DictParameter(),
        },
        access="launch",
        api=True,
    )
    def api_render_snippet(self, request, snippet_id, objects, config):
        snippet = self.get_object_or_404(CommandSnippet, id=int(snippet_id))
        r = {}
        for mo in objects:
            config["object"] = mo
            r[mo.id] = snippet.expand(config)
        return r

    @view(
        url="^render/action/(?P<action_id>[0-9a-f]{24})/$",
        method=["POST"],
        validate={
            "objects": ListOfParameter(element=ModelParameter(ManagedObject)),
            "config": DictParameter(),
        },
        access="launch",
        api=True,
    )
    def api_render_action(self, request, action_id, objects, config):
        action = self.get_object_or_404(Action, id=action_id)
        r = {}
        for mo in objects:
            r[mo.id] = action.expand(mo, **config)
        return r
