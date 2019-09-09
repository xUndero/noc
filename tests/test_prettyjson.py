# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# noc.core.prettyjson unittests
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest

# NOC modules
from noc.core.prettyjson import to_json


@pytest.mark.parametrize(
    "config, expected",
    [
        ("\n", True),
    ],
)
def test_prettyjson(config, expected):
    json_string = {"key1": "value1", "key2": "value2", "key3": "value3"}
    prettyjson = to_json(json_string)
    assert prettyjson.endswith(config) == expected
