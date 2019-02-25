# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# noc.lib.text tests
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Thirt-party modules
import pytest
# NOC modules
from noc.lib.text import parse_table


@pytest.mark.parametrize("value,kwargs,expected", [
    (
        "First Second Third\n"
        "----- ------ -----\n"
        "a     b       c\n"
        "ddd   eee     fff\n",
        {},
        [["a", "b", "c"], ["ddd", "eee", "fff"]]
    ),
    (
        "First Second Third\n"
        "----- ------ -----\n"
        "a             c\n"
        "ddd   eee     fff\n",
        {},
        [["a", "", "c"], ["ddd", "eee", "fff"]]
    ),
    (
        "VLAN Status  Name                             Ports\n"
        "---- ------- -------------------------------- ---------------------------------\n"
        "4090 Static  VLAN4090                         f0/5, f0/6, f0/7, f0/8, g0/9\n"
        "                                              g0/10\n",
        {"allow_wrap": True, "n_row_delim": ", "},
        [["4090", "Static", "VLAN4090", "f0/5, f0/6, f0/7, f0/8, g0/9, g0/10"]]
    ),
    (
        " MSTI ID     Vid list\n"
        " -------     -------------------------------------------------------------\n"
        "    CIST     1-11,15-122,124-250,253,257-300,302-445,447-709\n"
        "             ,720-759,770-879,901-3859,3861-4094\n"
        "       1     12-14,123,251-252,254-256,301,446,710-719,760-769,\n"
        "             880-900,3860\n",
        {"allow_wrap": True, "n_row_delim": ","},
        [
            ["CIST", "1-11,15-122,124-250,253,257-300,302-445,447-709,720-759,770-879,901-3859,3861-4094"],
            ["1", "12-14,123,251-252,254-256,301,446,710-719,760-769,880-900,3860"]
        ]
    ),
    (
        "Vlan    Mac Address       Type       Ports\n"
        "----    -----------       ----       -----\n"
        "All\t1111.2222.3333\t  STATIC     CPU\n"
        "611\t1234.2222.2222\t  DYNAMIC    g0/2\n"
        "611\t2345.3333.3333\t  DYNAMIC    g0/2\n"
        "611\t3456.4444.4444\t  DYNAMIC    g0/2\n"
        "1\t4567.5555.5555\t  DYNAMIC    g0/1\n"
        "1\t5678.6666.6666\t  DYNAMIC    g0/2\n"
        "611\t0050.7777.7777\t  DYNAMIC    g0/2\n"
        "611\t0050.8888.8888\t  DYNAMIC    g0/2\n"
        "611\t0050.9999.9999\t  DYNAMIC    g0/2\n",
        {"allow_extend": True, "n_row_delim": ","},
        [
            ["All", "1111.2222.3333", "STATIC", "CPU"],
            ["611", "1234.2222.2222", "DYNAMIC", "g0/2"],
            ["611", "2345.3333.3333", "DYNAMIC", "g0/2"],
            ["611", "3456.4444.4444", "DYNAMIC", "g0/2"],
            ["1", "4567.5555.5555", "DYNAMIC", "g0/1"],
            ["1", "5678.6666.6666", "DYNAMIC", "g0/2"],
            ["611", "0050.7777.7777", "DYNAMIC", "g0/2"],
            ["611", "0050.8888.8888", "DYNAMIC", "g0/2"],
            ["611", "0050.9999.9999", "DYNAMIC", "g0/2"]
        ]
    )
])
def test_parse_table(value, kwargs, expected):
    assert parse_table(value, **kwargs) == expected
