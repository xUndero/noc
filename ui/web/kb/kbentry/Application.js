//---------------------------------------------------------------------
// kb.kbentry application
//---------------------------------------------------------------------
// Copyright (C) 2007-2013 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.kb.kbentry.Application");

Ext.define("NOC.kb.kbentry.Application", {
    extend: "NOC.core.ModelApplication",
    layout: "card",
    requires: [
        "NOC.kb.kbentry.Model",
        "NOC.main.language.LookupField",
        "NOC.main.ref.kbparser.LookupField"
    ],
    model: "NOC.kb.kbentry.Model",
    search: true,
    initComponent: function() {
        var me = this;

        me.historyButton = Ext.create("Ext.button.Button", {
            text: __("History"),
            glyph: NOC.glyph.history,
            scope: me,
            handler: me.onHistory
        });

        me.ITEM_HISTORY = me.registerItem("NOC.kb.kbentry.HistoryPanel");

        Ext.apply(me, {
            columns: [
                {
                    xtype: "glyphactioncolumn",
                    width: 20,
                    sortable: false,
                    items: [
                        {
                            glyph: NOC.glyph.eye,
                            tooltip: __("Show KB"),
                            handler: me.onShowKB
                        }
                    ]
                },
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
                    name: "markup_language",
                    xtype: "main.ref.kbparser.LookupField",
                    fieldLabel: __("Markup Language"),
                    allowBlank: false
                },
                {
                    name: "tags",
                    xtype: "tagsfield",
                    fieldLabel: __("Tags"),
                    allowBlank: true
                }
            ],
            formToolbar: [
                me.historyButton
            ]
        });
        me.callParent();
    },
    onShowKB: function(view, rowIndex, colIndex, item, e, record) {
        window.open(
            "/api/card/view/kb/" + record.id + "/"
        );
    },
    onHistory: function() {
        var me = this;
        me.previewItem(me.ITEM_HISTORY, me.currentRecord);
    }
});