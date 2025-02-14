# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# HTTP Dahua Auth Middleware
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import ujson
import hashlib
import base64

# NOC modules
from noc.core.script.http.middleware.base import BaseMiddleware
from noc.core.http.client import fetch_sync


class DahuaAuthMiddeware(BaseMiddleware):
    """
    Append HTTP Digest authorisation headers
    """

    name = "dahuaauth"

    def __init__(self, http):
        super(DahuaAuthMiddeware, self).__init__(http)
        self.user = self.http.script.credentials.get("user")
        self.password = self.http.script.credentials.get("password")

    def get_auth(self, params):
        """
        Web JS
        i.getAuth = function(a, b, c) {
            switch (c = c || j.encryption) {
            case "Basic":
                return Base64.encode(a + ":" + b);
            case "Default":
                return hex_md5(a + ":" + j.random + ":" + hex_md5(a + ":" + j.realm + ":" + b));
            default:
                return b
            }
        :param params: response params dictionary
        :type params: dict
        :return: Password string
        :rtype: str
        """
        if params["encryption"] == "Basic":
            return base64.b64encode("%s:%s" % (self.user, self.password))
        elif params["encryption"] == "Default":
            A1 = (
                hashlib.md5("%s:%s:%s" % (self.user, params["realm"], self.password))
                .hexdigest()
                .upper()
            )
            return hashlib.md5("%s:%s:%s" % (self.user, params["random"], A1)).hexdigest().upper()
        else:
            return self.password

    def process_post(self, url, body, headers):
        """
        Dahua Web auth procedure
        :param url:
        :param body:
        :param headers:
        :return:
        """
        if self.http.session_id:
            body["session"] = self.http.session_id
            return url, body, headers
        if not headers:
            headers = {}
        # First query - /RPC2_Login
        auth_url = self.http.get_url("/RPC2_Login")
        code, resp_headers, result = fetch_sync(
            auth_url,
            method="POST",
            body={
                "method": "global.login",
                "params": {
                    "userName": self.user,
                    "password": "",
                    "clientType": "Web3.0",
                    "loginType": "Direct",
                },
                "id": self.http.request_id,
            },
            headers=headers,
            request_timeout=60,
            follow_redirects=True,
            allow_proxy=False,
            validate_cert=False,
        )
        r = ujson.loads(result)
        session = r["session"]
        self.http.set_session_id(session)
        password = self.get_auth(r["params"])

        code, resp_headers, result = fetch_sync(
            auth_url,
            method="POST",
            body={
                "method": "global.login",
                "params": {
                    "userName": self.user,
                    "password": password,
                    "clientType": "Web3.0",
                    "loginType": "Direct",
                },
                "id": self.http.request_id,
                "session": session,
            },
            headers=headers,
            request_timeout=60,
            follow_redirects=True,
            allow_proxy=False,
            validate_cert=False,
        )
        self.http.request_id += 2
        body["session"] = self.http.session_id
        return url, body, headers
