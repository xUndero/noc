# ----------------------------------------------------------------------
# BI Models loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import os
# NOC modules
from noc.core.clickhouse.model import Model
from noc.config import config

BASE_PREFIX = os.path.join("bi", "models")
PATHS = config.get_customized_paths(BASE_PREFIX)


def iter_bi_model():
    global PATHS

    for path in PATHS:
        if not os.path.exists(path):
            continue
        for f in os.listdir(path):
            if f.startswith("_") or not f.endswith(".py"):
                continue
            mn = f[:-3]

            b, _ = path.split(BASE_PREFIX)
            if b:
                basename = os.path.basename(os.path.dirname(b))
            else:
                basename = "noc"
            model = Model.get_model_class(mn, basename=basename)
            if model:
                yield model
