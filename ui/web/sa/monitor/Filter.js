//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------

console.debug('Defining NOC.sa.monitor.Filter');
Ext.define('NOC.sa.monitor.Filter', {
    extend: 'NOC.core.filter.Filter',
    alias: 'widget.monitor.Filter',
    controller: 'monitor.filter',
    requires: [
        'NOC.sa.monitor.FilterController'
    ],
    initComponent: function() {
        Ext.apply(this, {
            items: [
                {
                    xtype: 'container',
                    layout: 'hbox',
                    items: [
                        {
                            xtype: 'button',
                            toggleGroup: 'status',
                            text: __('Suspend'),
                            value: 's',
                            reference: 's-btn',
                            handler: 'setFilter'
                        },
                        {
                            xtype: 'button',
                            toggleGroup: 'status',
                            text: __('Wait'),
                            value: 'W',
                            reference: 'W-btn',
                            handler: 'setFilter'
                        }
                    ]
                }
            ].concat(this.items)
        });
        this.callParent(arguments);
    }
});
