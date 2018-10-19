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
            urls = [];
        me.currentId = data.id;
        urls.push("/ui/pkg/leaflet/leaflet.js");
        urls.push("/ui/pkg/leaflet/leaflet.css");
        new_load_scripts(urls, me, function() {
            me.createMap(data);
        });
    },
    //
    createLayer: function(query, layer) {
        var me = this;
        Ext.Ajax.request({
            url: "/inv/inv/plugin/map/layers/" + query,
            method: 'GET',
            scope: me,
            success: function(response) {
                var me = this, addLayer,
                    geoJSON = Ext.decode(response.responseText);
                if(!Ext.isFunction(layer.hasLayer)) {
                    addLayer = L.geoJSON(geoJSON, {
                        nocCode: layer.code,
                        nocName: layer.name,
                        pointToLayer: function(geoJsonPoint, latlng) {
                            return L.circle(latlng, {
                                color: layer.fill_color,
                                fillColor: layer.fill_color,
                                fillOpacity: 1,
                                radius: 28
                            });
                        },
                        style: function(json) {
                            return {
                                fillColor: layer.fill_color,
                                strokeColor: layer.stroke_color,
                                weight: layer.stroke_width
                            };
                        },
                        filter: function(geoJsonFeature) {
                            var zoom = me.map.getZoom();
                            return (zoom >= layer.min_zoom) && (zoom <= layer.max_zoom)
                        }
                    });
                    if(layer.is_visible) {
                        addLayer.bindPopup(Ext.bind(me.onFeatureClick, me)).addTo(me.map);
                    }
                    me.mapControl.addOverlay(addLayer, layer.name);
                    addLayer.on("add", me.visibilityHandler);
                    addLayer.on("remove", me.visibilityHandler);
                } else { // modify layer
                    // console.log("modify layer", geoJSON);
                    layer.clearLayers();
                    layer.addData(geoJSON);
                }
            },
            failure: function() {
                NOC.error(__('Failed to get layer'));
            }
        });
    },
    //
    getQuery: function(layerCode) {
        return Ext.String.format(layerCode + "/?bbox={0},EPSG%3A4326", this.map.getBounds().toBBoxString());
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
        me.map.on('moveend', Ext.bind(me.reloadLayers, me));
        //
        me.mapControl = L.control.layers();
        me.mapControl.addTo(me.map);
        Ext.each(data.layers, function(layer) {
            me.createLayer(me.getQuery(layer.code), layer);
        });
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
    },
    //
    reloadLayers: function() {
        var me = this;
        me.map.eachLayer(function(layer) {
            if(layer.hasOwnProperty("options") && layer.options.hasOwnProperty("nocCode")) {
                me.createLayer(me.getQuery(layer.options.nocCode), layer);
            }
        });
    }
});
