//---------------------------------------------------------------------
// inv.inv Leaflet Map panel
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.inv.inv.plugins.map.LeafMapPanel");

Ext.define("NOC.inv.inv.plugins.map.LeafMapPanel", {
    extend: "Ext.panel.Panel",
    requires: [],
    title: __("LeafLet"),
    closable: false,
    layout: "fit",
    autoScroll: true,

    initComponent: function() {
        var me = this;
        //
        me.infoTemplate = '<b>{0}</b><br><i>{1}</i><br><hr><a id="{2}" href="api/card/view/object/{3}/" target="_blank">Show...</a>';
        // Layers holder
        me.layers = [];
        //
        me.centerButton = Ext.create("Ext.button.Button", {
            tooltip: __("Center to object"),
            glyph: NOC.glyph.location_arrow,
            scope: me,
            handler: me.centerToObject
        });
        // Map panel
        Ext.apply(me, {
            dockedItems: [{
                xtype: "toolbar",
                dock: "top",
                items: [
                    me.centerButton
                ]
            }],
            items: [
                {
                    xtype: "panel",
                    // Generate unique id
                    html: "<div id='leaf-map-" + me.id + "' style='width: 100%; height: 100%;'></div>"
                }
            ]
        });
        me.callParent();
    },
    //
    preview: function(data) {
        var me = this,
            urls = [
                "/ui/pkg/leaflet/leaflet.js",
                "/ui/pkg/leaflet/leaflet.css"
            ];
        me.currentId = data.id;
        new_load_scripts(urls, me, function() {
            me.createMap(data);
        });
    },
    //
    createLayer: function(cfg) {
        var me = this,
            layer;
        layer = L.geoJSON({
            "type": "FeatureCollection",
            "features": []
        }, {
            nocCode: cfg.code,
            nocMinZoom: cfg.min_zoom,
            nocMaxZoom: cfg.max_zoom,
            pointToLayer: function(geoJsonPoint, latlng) {
                return L.circle(latlng, {
                    color: cfg.fill_color,
                    fillColor: cfg.fill_color,
                    fillOpacity: 1,
                    radius: 28
                });
            },
            style: function(json) {
                return {
                    color: cfg.fill_color,
                    fillColor: cfg.fill_color,
                    strokeColor: cfg.stroke_color,
                    weight: cfg.stroke_width
                };
            },
            filter: function(geoJsonFeature) {
                // Remove invisible layers on zoom
                var zoom = me.map.getZoom();
                return (zoom >= cfg.min_zoom) && (zoom <= cfg.max_zoom)
            }
        });
        layer.addTo(me.map);
        me.mapControl.addOverlay(layer, cfg.name);
        layer.on("add", me.visibilityHandler);
        layer.on("remove", me.visibilityHandler);
        return layer;
    },
    //
    loadLayer: function(layer) {
        var me = this,
            zoom = me.map.getZoom();
        if((zoom < layer.options.nocMinZoom) || (zoom > layer.options.nocMaxZoom)) {
            // Not visible
            layer.clearLayers();
            return;
        }
        if(me.map.hasLayer(layer)) {
            Ext.Ajax.request({
                url: "/inv/inv/plugin/map/layers/" + me.getQuery(layer.options.nocCode),
                method: 'GET',
                scope: me,
                success: function(response) {
                    var data = Ext.decode(response.responseText);
                    layer.clearLayers();
                    if(!Ext.Object.isEmpty(data)) {
                        layer.addData(data)
                    }
                },
                failure: function() {
                    NOC.error(__('Failed to get layer'));
                }
            });
        }
    },
    //
    getQuery: function(layerCode) {
        return Ext.String.format(layerCode + "/?bbox={0},EPSG%3A4326", this.map.getBounds().toBBoxString());
    },
    //
    refresh: function() {
        var me = this;
        Ext.each(me.layers, function(layer) {
            me.loadLayer(layer);
        });
    },
    //
    createMap: function(data) {
        var me = this,
            osm,
            mapDiv = "leaf-map-" + me.id,
            mapDom = Ext.select("#" + mapDiv).elements[0];
        osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {});
        me.center = [data.y, data.x];
        me.contextMenuData = data.add_menu;
        me.initScale = data.zoom;
        //
        me.map = L.map(mapDom).setView(me.center, me.initScale);
        me.map.addLayer(osm);
        me.map.on('contextmenu', Ext.bind(me.onContextMenu, me));
        me.map.on('moveend', Ext.bind(me.refresh, me));
        //
        me.mapControl = L.control.layers();
        me.mapControl.addTo(me.map);
        me.layers = [];
        Ext.each(data.layers, function(cfg) {
            me.layers.push(me.createLayer(cfg));
        });
        me.refresh();
    },
    //
    visibilityHandler: function(e) {
        // console.log(Ext.String.format("visibility {0} is {1}", e.target.options.nocCode, (e.type === "add") ? "Yes" : "No"));
        Ext.Ajax.request({
            url: "/inv/inv/plugin/map/layer_visibility/",
            method: "POST",
            jsonData: {
                layer: e.target.options.nocCode,
                status: e.type === "add"
            },
            failure: function() {
                NOC.error(__("Failed to change layer settings"));
            }
        });

    },
    //
    centerToObject: function() {
        var me = this;
        me.map.setView(me.center, me.initScale);
    },
    //
    onFeatureClick: function(e) {
        var me = this, result;
        if(!e.feature.properties.object) {
            return __("no object");
        }
        Ext.Ajax.request({
            url: "/inv/inv/" + e.feature.properties.object + "/plugin/map/object_data/",
            method: "GET",
            async: false,
            scope: me,
            success: function(response) {
                var me = this;
                result = me.showObjectPopup(e.feature, Ext.decode(response.responseText));
            },
            failure: function() {
                result = __("Failed to get data");
            }
        });
        return result;
    },
    //
    showObjectPopup: function(feature, data) {
        var me = this,
            showLinkId = "noc-leaf-tip-show-link-" + me.id,
            text;
        text = Ext.String.format(me.infoTemplate, data.name, data.model, showLinkId, data.id);
        if(!Ext.Object.isEmpty(data.moname)) {
            var listLength = 10;
            var objects = Object.keys(data.moname).map(function(key) {
                return '<li><a href="api/card/view/managedobject/' + key + '/" target="_blank">'
                    + data.moname[key].moname.replace(/\s/g, "&nbsp;") + '</a></li>'
            }).slice(0, listLength).join("");
            text += "<br><hr>Objects:<br><ul>" + objects + "</ul>";
            if(Object.keys(data.moname).length >= listLength) {
                text += "<br>More...";
            }
        }
        return text;
    },
    //
    onContextMenu: function(event) {
        var me = this,
            m = me.getContextMenu();
        me.event = event;
        m.showAt(event.originalEvent.clientX, event.originalEvent.clientY);
    },
    //
    getContextMenu: function() {
        var me = this,
            addHandler = function(items) {
                Ext.each(items, function(item) {
                    if(item.hasOwnProperty("menu")) {
                        addHandler(item.menu);
                    } else if(item.hasOwnProperty("objectTypeId")) {
                        item.listeners = {
                            scope: me,
                            click: me.onContextMenuAdd
                        }
                    }
                });
                return items;
            };
        // Return cached
        if(me.contextMenu) {
            return me.contextMenu;
        }
        me.contextMenu = Ext.create("Ext.menu.Menu", {
            renderTo: me.mapDom,
            items: [
                {
                    text: __("Add"),
                    menu: addHandler(me.contextMenuData)
                }
            ]
        });
        return me.contextMenu;
    },
    //
    onContextMenuAdd: function(item) {
        var me = this;
        Ext.create("NOC.inv.inv.plugins.map.AddObjectForm", {
            app: me,
            objectModelId: item.objectTypeId,
            objectModelName: item.text,
            newPosition: {
                lon: me.event.latlng.lng,
                lat: me.event.latlng.lat,
                // ToDo remove
                toString: function() {
                    return "lon=" + this.lon + ",lat=" + this.lat
                }
            },
            positionSRID: "EPSG:4326"
        }).show();
    }
});
