//---------------------------------------------------------------------
// Header
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.desktop.HeaderPanel");
Ext.define("NOC.main.desktop.HeaderPanel", {
    extend: "Ext.Panel",
    requires: [
        "Ext.ux.form.SearchField"
    ],
    region: "north",
    layout: {
        type: "hbox",
        align: "middle"
    },
    pollingInterval: 3600000,
    localStoreName: "header-last-update",
    border: false,
    bodyStyle: {
        "background-color": NOC.settings.branding_background_color + " !important",
        "color": NOC.settings.branding_color
    },
    collapsible: true,
    animCollapse: true,
    collapseMode: "mini",
    //split: true,
    header: false,
    app: null,
    bodyPadding: 4,
    //
    initComponent: function() {
        var me = this;
        // Last update menu
        me.lastUpdateButton = Ext.create("Ext.button.Button", {
            hidden: true,
            text: __("Show remote sync time"),
            margin: "0 5"
        });
        // User menu
        me.userMenuButton = Ext.create("Ext.button.Button", {
            text: __("Anonymous"),
            scale: "small",
            glyph: NOC.glyph.user,
            hidden: true,
            menu: [
                {
                    text: __("About system ..."),
                    glyph: NOC.glyph.question_circle,
                    scope: me.app,
                    handler: me.app.onAbout
                },
                "-",
                {
                    text: __("User profile ..."),
                    glyph: NOC.glyph.cog,
                    scope: me.app,
                    handler: me.app.onUserProfile
                },
                {
                    itemId: "header_menu_change_password",
                    text: __("Change password ..."),
                    disabled: true, // Changed on login
                    glyph: NOC.glyph.lock,
                    scope: me.app,
                    handler: me.app.onChangeCredentials
                },
                "-",
                {
                    text: __("Logout"),
                    glyph: NOC.glyph.power_off,
                    scope: me.app,
                    handler: me.app.onLogout
                }
            ]
        });
        // fix: fake field for Chrome ignores autocomplete=“off”
        me.emptyField = Ext.create("Ext.form.field.Text", {
            itemId: "empty",
            name: "empty",
            inputType: "password",
            hidden: true
        });
        Ext.apply(me, {
            items: [
                // NOC logo
                Ext.create("Ext.Img", {
                    src: NOC.settings.logo_url,
                    style: {
                        width: NOC.settings.logo_width + "px",
                        height: NOC.settings.logo_height + "px"
                    }
                }),
                // Bold NOC|
                {
                    xtype: "container",
                    html: "&nbsp;" + NOC.settings.brand + "|&nbsp;",
                    style: {
                        fontSize: "18px",
                        fontWeight: "bold"
                    },
                    border: false
                },
                // Installation name
                {
                    xtype: "container",
                    flex: 1,
                    html: NOC.settings.installation_name,
                    style: {
                        fontSize: "18px"
                    },
                    border: false
                },
                me.emptyField,
                // Last update
                me.lastUpdateButton,
                // User menu
                me.userMenuButton,
                // Search field
                {
                    xtype: "searchfield",
                    padding: "0 0 0 4",
                    explicitSubmit: true,
                    scope: me,
                    handler: me.app.onSearch,
                    hidden: !NOC.settings.enable_search
                }
            ]
        });
        me.userProfileItem = me.userMenuButton.menu.getComponent("header_menu_change_password");
        if(NOC.settings.enable_remote_system_last_extract_info) {
            me.lastUpdateButton.show();
            Ext.TaskManager.start({
                run: me.pollingTask,
                interval: me.pollingInterval,
                scope: me
            });
        }
        me.callParent();
    },
    // Change displayed username
    setUserName: function(username) {
        var me = this;
        me.userMenuButton.setText(username);
    },
    //
    hideUserMenu: function() {
        var me = this;
        me.userMenuButton.hide();
    },
    //
    showUserMenu: function(canChangeCredentials) {
        var me = this;
        me.userProfileItem.setDisabled(!canChangeCredentials);
        me.userMenuButton.show();
    },
    //
    pollingTask: function() {
        var me = this;
        Ext.Ajax.request({
            url: "/main/remotesystem/brief_lookup/",
            method: "GET",
            scope: me,
            success: function(response) {
                var data = Ext.decode(response.responseText);
                this.lastUpdateButton.setMenu({
                    onMouseOver: Ext.emptyFn,
                    items: Ext.Array.map(data, function(e) {
                        return {
                            text: __(e.label + " " + e.last_successful_load)
                        }
                    })
                }, true);
            },
            failure: function() {
                NOC.error(__("Failed to get remote sync time"));
            }
        });
    }
});
