//---------------------------------------------------------------------
// fm.alarm application
//---------------------------------------------------------------------
// Copyright (C) 2007-2013 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.fm.alarm.Application");

Ext.define("NOC.fm.alarm.Application", {
    extend: "NOC.core.Application",
    requires: [
        "NOC.fm.alarm.templates.Overview",
        "NOC.fm.alarm.templates.Help",
        "NOC.fm.alarm.templates.Data"
    ],
    layout: "card",
    STATUS_MAP: {
        A: "Active",
        C: "Archived"
    },
    pollingInterval: 30000,
    //
    initComponent: function() {
        var me = this;
        me.currentQuery = {status: "A"};
        me.pollingTaskHandler = Ext.bind(me.pollingTask, me);
        me.store = Ext.create("NOC.core.ModelStore", {
            model: "NOC.fm.alarm.Model",
            autoLoad: false,
            pageSize: 1,
            customFields: [],
            filterParams: {
                status: "A",
                collapse: 1
            }
        });

        me.typeCombo = Ext.create("Ext.form.ComboBox", {
            fieldLabel: "State",
            labelWidth: 30,
            queryMode: "local",
            displayField: "name",
            valueField: "id",
            store: Ext.create("Ext.data.Store", {
                fields: ["id", "name"],
                data: [
                    {id: "A", name: "Active"},
                    {id: "C", name: "Archived"},
                ]
            }),
            value: "A",
            width: 110,
            listeners: {
                select: {
                    scope: me,
                    fn: me.onChangeFilter
                }
            }
        });

        me.objectCombo = Ext.create("NOC.sa.managedobject.LookupField", {
            fieldLabel: "Object",
            labelWidth: 40,
            width: 200,
            listeners: {
                scope: me,
                select: me.onChangeFilter,
                clear: me.onChangeFilter
            }
        });

        me.alarmClassCombo = Ext.create("NOC.fm.alarmclass.LookupField", {
            fieldLabel: "Class",
            labelWidth: 40,
            width: 300,
            listeners: {
                scope: me,
                select: me.onChangeFilter,
                clear: me.onChangeFilter
            }
        });

        me.fromDateField = Ext.create("Ext.form.field.Date", {
            fieldLabel: "From",
            labelWidth: 35,
            format: "d.m.Y",
            width: 130,
            listeners: {
                scope: me,
                select: me.onChangeFilter
            }
        });

        me.toDateField = Ext.create("Ext.form.field.Date", {
            fieldLabel: "To",
            labelWidth: 25,
            format: "d.m.Y",
            width: 120,
            listeners: {
                scope: me,
                select: me.onChangeFilter
            }
        });

        me.expandButton = Ext.create("Ext.button.Button", {
            text: "Expand",
            tooltip: "Show/collapse children alarms",
            enableToggle: true,
            scope: me,
            handler: me.onChangeFilter
        });

        me.gridPanel = Ext.create("Ext.grid.Panel", {
            store: me.store,
            features: [{
                ftype: "selectable",
                id: "selectable"
            }],
            border: false,
            stateful: true,
            stateId: "fm.alarm-grid",
            plugins: [Ext.create("Ext.ux.grid.AutoSize")],
            dockedItems: [
                {
                    xtype: "toolbar",
                    dock: "top",
                    items: [
                        me.typeCombo,
                        me.objectCombo,
                        me.alarmClassCombo,
                        me.fromDateField,
                        me.toDateField,
                        me.expandButton
                    ]
                },
                {
                    xtype: "pagingtoolbar",
                    store: me.store,
                    dock: "bottom",
                    displayInfo: true
                }
            ],
            columns: [
                {
                    text: "ID",
                    dataIndex: "id",
                    width: 150
                },
                {
                    text: "Status",
                    dataIndex: "status",
                    width: 50,
                    renderer: NOC.render.Choices(me.STATUS_MAP),
                    hidden: true
                },
                {
                    text: "Time",
                    dataIndex: "timestamp",
                    width: 100,
                    renderer: NOC.render.DateTime
                },
                {
                    text: "Object",
                    dataIndex: "managed_object",
                    width: 200,
                    renderer: NOC.render.Lookup("managed_object")
                },
                {
                    text: "Class",
                    dataIndex: "alarm_class",
                    width: 300,
                    renderer: NOC.render.Lookup("alarm_class")
                },
                {
                    text: "Subject",
                    dataIndex: "subject",
                    flex: 1
                },
                {
                    text: "Events",
                    dataIndex: "events",
                    width: 30,
                    align: "right"
                }
            ],
            selModel: Ext.create("Ext.selection.CheckboxModel"),
            listeners: {
                itemdblclick: {
                    scope: me,
                    fn: me.onSelectAlarm
                }
            },
            viewConfig: {
                getRowClass: Ext.bind(me.getRowClass, me)
                /* listeners: {
                    scope: me,
                    cellclick: me.onCellClick
                }*/
            }
        });
        //
        me.alarmPanel = Ext.create("NOC.fm.alarm.AlarmPanel", {
            app: me
        });
        me.ITEM_GRID = me.registerItem(me.gridPanel);
        me.ITEM_FORM = me.registerItem(me.alarmPanel);
        Ext.apply(me, {
            items: me.getRegisteredItems()
        });
        me.callParent();
        //
        me.startPolling();
    },
    //
    reloadStore: function() {
        var me = this;
        if(me.currentQuery)
            me.store.setFilterParams(me.currentQuery);
        me.store.load();
    },
    //
    onChangeFilter: function() {
        var me = this,
            q = {},
            setIf = function(k, v) {
                if(v) {
                    q[k] = v;
                }
            }

        // Status
        q.status = me.typeCombo.getValue();
        // Object
        setIf("managed_object", me.objectCombo.getValue());
        // Class
        setIf("alarm_class", me.alarmClassCombo.getValue());
        // From Date
        setIf("timestamp__gte", me.fromDateField.getValue());
        // To Date
        setIf("timestamp__lte", me.toDateField.getValue());
        // Expand
        if(!me.expandButton.pressed) {
            q.collapse = 1;
        }
        me.currentQuery = q;
        me.reloadStore();
    },
    // Return Grid's row classes
    getRowClass: function(record, index, params, store) {
        var c = record.get("row_class");
        if(c) {
            return c;
        } else {
            return "";
        }
    },
    //
    showGrid: function() {
        var me = this;
        me.getLayout().setActiveItem(0);
        me.reloadStore();
        me.startPolling();
    },
    //
    onSelectAlarm: function(grid, record, item, index) {
        var me = this;
        me.stopPolling();
        me.getLayout().setActiveItem(1);
        me.alarmPanel.showAlarm(record.get("id"));
    },
    //
    pollingTask: function() {
        var me = this;
        me.store.load();
    },
    //
    startPolling: function() {
        var me = this;
        me.pollingTaskId = Ext.TaskManager.start({
            run: me.pollingTaskHandler,
            interval: me.pollingInterval
        });
    },
    //
    stopPolling: function() {
        var me = this;
        Ext.TaskManager.stop(me.pollingTaskId);
    },
    //
    showForm: function() {
        var me = this;
        me.showItem(me.ITEM_FORM);
    }
});
