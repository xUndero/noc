//---------------------------------------------------------------------
// inv.inv application
//---------------------------------------------------------------------
// Copyright (C) 2007-2013 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.kb.kbentry2.Application");

Ext.define("NOC.kb.kbentry2.Application", {
    extend: "NOC.core.ModelApplication",
    layout: "card",
    requires: [
        "NOC.kb.kbentry2.Model",
        "NOC.main.language.LookupField"
    ],
    model: "NOC.kb.kbentry2.Model",
    search: true,
    initComponent: function() {
        var me = this;

        Ext.apply(me, {
            columns: [
                {
                    text: __("Subject"),
                    dataIndex: "subject"
                },
                {
                    text: __("Language"),
                    dataIndex: "language",
                    renderer: NOC.render.Lookup("language")
                },
                {
                    text: __("Tags"),
                    dataIndex: "tags",
                    renderer: NOC.render.Tags
                }
            ],
            fields: [
                {
                    name: "subject",
                    xtype: "textfield",
                    fieldLabel: __("Subject"),
                    allowBlank: false
                },
                {
                    name: "body",
                    xtype: "htmleditor",
                    fieldLabel: __("Body"),
                    allowBlank: false
                },
                {
                    name: "language",
                    xtype: "main.language.LookupField",
                    fieldLabel: __("Language"),
                    allowBlank: false
                },
                {
                    name: "tags",
                    xtype: "tagsfield",
                    fieldLabel: __("Tags"),
                    allowBlank: true
                }
            ]
        });
        me.callParent();
    }
});