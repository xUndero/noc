//---------------------------------------------------------------------
//  Probe Config
//---------------------------------------------------------------------
// Generated by ./noc update-probe-config
//---------------------------------------------------------------------
// Copyright (C) 2007-2014 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.metricconfig.pm.probes.db.postgres.PostgresConfig");

Ext.define("NOC.metricconfig.pm.probes.db.postgres.PostgresConfig", {
    extend: "NOC.core.ProbeConfig",
    form: [
        {
            name: "host",
            xtype: "textfield",
            fieldLabel: "host",
            allowBlank: false
        },
        {
            name: "port",
            xtype: "textfield",
            fieldLabel: "port",
            allowBlank: true
        },
        {
            name: "database",
            xtype: "textfield",
            fieldLabel: "database",
            allowBlank: false
        },
        {
            name: "user",
            xtype: "textfield",
            fieldLabel: "user",
            allowBlank: true
        },
        {
            name: "password",
            xtype: "textfield",
            fieldLabel: "password",
            allowBlank: true
        }
    ]
});
