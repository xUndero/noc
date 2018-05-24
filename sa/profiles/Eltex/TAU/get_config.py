# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.TAU.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig


class Script(BaseScript):
    name = "Eltex.TAU.get_config"
    interface = IGetConfig

    def execute(self):
        config = self.cli("config")
        show = self.cli("show")
        exit = self.cli("exit")
        return self.cleaned_config(show)
