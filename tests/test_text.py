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
        'Vlan    Mac Address       Type       Ports\n'
        '----    -----------       ----       -----\n'
        'All\t1111.2222.3333\t  STATIC     CPU\n'
        '611\t1111.2223.3efc\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.3cdc\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.4010\t  DYNAMIC    g0/2\n'
        '1\t1111.2224.1fd8\t  DYNAMIC    g0/1\n'
        '1\t1111.2225.0bb1\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.6bfc\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.42d8\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.6bf8\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.42dc\t  DYNAMIC    g0/2\n'
        '611\t1111.2226.0001\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.3cd8\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.3ef8\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.4014\t  DYNAMIC    g0/2\n'
        '611\t1111.2227.3480\t  DYNAMIC    g0/2\n'
        '1\t1111.2228.a16d\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.38e0\t  DYNAMIC    g0/2\n'
        '1\t1111.2229.a16c\t  DYNAMIC    g0/2\n'
        '611\t1111.2223.38e4\t  DYNAMIC    g0/2\n'
        '611\t1111.222a.2e1e\t  DYNAMIC    g0/2\n',
        {"expand_columns": True},
        [
            ["All", "1111.2222.3333", "STATIC", "CPU"],
            ["611", "1111.2223.3efc", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.3cdc", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.4010", "DYNAMIC", "g0/2"],
            ["1", "1111.2224.1fd8", "DYNAMIC", "g0/1"],
            ["1", "1111.2225.0bb1", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.6bfc", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.42d8", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.6bf8", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.42dc", "DYNAMIC", "g0/2"],
            ["611", "1111.2226.0001", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.3cd8", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.3ef8", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.4014", "DYNAMIC", "g0/2"],
            ["611", "1111.2227.3480", "DYNAMIC", "g0/2"],
            ["1", "1111.2228.a16d", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.38e0", "DYNAMIC", "g0/2"],
            ["1", "1111.2229.a16c", "DYNAMIC", "g0/2"],
            ["611", "1111.2223.38e4", "DYNAMIC", "g0/2"],
            ["611", "1111.222a.2e1e", "DYNAMIC", "g0/2"]
        ]
    )
])
def test_parse_table(value, kwargs, expected):
    assert parse_table(value, **kwargs) == expected
