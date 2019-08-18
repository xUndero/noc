# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# User Manager
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import re

# Third-party modules
from django.conf import settings
from django.http import HttpResponse

# NOC modules
from noc.lib.app.site import site
from noc.lib.app.extmodelapplication import ExtModelApplication, view
from noc.aaa.models.permission import Permission
from noc.sa.interfaces.base import StringParameter
from noc.core.translation import ugettext as _
from noc.aaa.models.user import User


class UsernameParameter(StringParameter):
    user_validate = re.compile(r"^[\w.@+-]+$")

    def clean(self, value):
        r = super(UsernameParameter, self).clean(value)
        match = self.user_validate.match(value)
        if not match:
            raise self.raise_error(
                value, msg="This value must contain only letters, digits and @/./+/-/_."
            )
        return r


class UserApplication(ExtModelApplication):
    model = User

    glyph = "user"
    menu = [_("Setup"), _("Users")]
    icon = "icon_user"
    title = _("Users")
    app_alias = "auth"
    query_condition = "icontains"
    query_fields = ["username"]
    default_ordering = ["username"]
    clean_fields = {
        "username": UsernameParameter(),
        "first_name": StringParameter(default=""),
        "last_name": StringParameter(default=""),
        "email": StringParameter(default=""),
    }
    ignored_fields = {"id", "bi_id", "password"}
    custom_m2m_fields = {"permissions": Permission}

    @classmethod
    def apps_permissions_list(cls):
        r = []
        apps = list(site.apps)
        perms = Permission.objects.values_list("name", flat=True)
        for module in [m for m in settings.INSTALLED_APPS if m.startswith("noc.")]:
            mod = module[4:]
            m = __import__("noc.services.web.apps.%s" % mod, {}, {}, "MODULE_NAME")
            for app in [app for app in apps if app.startswith(mod + ".")]:
                app_perms = sorted([p for p in perms if p.startswith(app.replace(".", ":") + ":")])
                a = site.apps[app]
                if app_perms:
                    for p in app_perms:
                        r += [
                            {
                                "module": m.MODULE_NAME,
                                "title": str(a.title),
                                "name": p,
                                "status": False,
                            }
                        ]
        return r

    @view(method=["GET"], url=r"^(?P<id>\d+)/?$", access="read", api=True)
    def api_read(self, request, id):
        """
        Returns dict with object's fields and values
        """
        try:
            o = self.queryset(request).get(**{self.pk: int(id)})
        except self.model.DoesNotExist:
            return HttpResponse("", status=self.NOT_FOUND)
        only = request.GET.get(self.only_param)
        if only:
            only = only.split(",")
        return self.response(self.instance_to_dict_get(o, fields=only), status=self.OK)

    def instance_to_dict_get(self, o, fields=None):
        r = super(UserApplication, self).instance_to_dict(o, fields)
        del r["password"]
        r["user_permissions"] = self.apps_permissions_list()
        current_perms = Permission.get_user_permissions(o)
        if current_perms:
            for p in r["user_permissions"]:
                if p["name"] in current_perms:
                    p["status"] = True
        return r

    def clean_list_data(self, data):
        """
        Finally process list_data result. Override to enrich with
        additional fields
        :param data:
        :return:
        """
        r = super(UserApplication, self).apply_bulk_fields(data=data)
        for x in r:
            if "password" in x:
                del x["password"]
        return r

    def update_m2m(self, o, name, values):
        if values is None:
            return  # Do not touch
        if name == "user_permissions":
            Permission.set_user_permissions(user=o, perms=values)
        else:
            super(UserApplication, self).update_m2m(o, name, values)

    @view(method=["GET"], url=r"^new_permissions/$", access="read", api=True)
    def api_read_permission(self, request):
        """
        Returns dict available permissions
        """
        return self.response(
            {"data": {"user_permissions": self.apps_permissions_list()}}, status=self.OK
        )

    @view(
        url=r"^(\d+)/password/$",
        method=["POST"],
        access="change",
        validate={"password": StringParameter(required=True)},
    )
    def view_change_password(self, request, object_id, password):
        """
        Change user's password
        :param request:
        :param object_id:
        :param password:
        :return:
        """
        if not request.user.is_superuser:
            return self.response_forbidden("Permission denied")
        user = self.get_object_or_404(self.model, pk=object_id)
        user.set_password(password)
        user.save()
        return self.response({"result": "Password changed", "status": True}, self.OK)

    def can_delete(self, user, obj=None):
        """Disable 'Delete' button"""
        return False
