const apps = [
    // aaa
    '../aaa/apikey/Application.js',
    '../aaa/group/Application.js',
    '../aaa/user/Application.js',
    // bi
    '../bi/dashboardlayout/Application.js',
    // cm
    '../cm/confdbquery/Application.js',
    '../cm/errortype/Application.js',
    '../cm/interfacevalidationpolicy/Application.js',
    '../cm/objectnotify/Application.js',
    '../cm/objectvalidationpolicy/Application.js',
    '../cm/validationpolicy/Application.js',
    '../cm/validationpolicysettings/Application.js',
    '../cm/validationrule/Application.js',
    // crm
    '../crm/subscriber/Application.js',
    '../crm/subscriberprofile/Application.js',
    '../crm/supplier/Application.js',
    '../crm/supplierprofile/Application.js',
    // dev
    '../dev/quiz/Application.js',
    '../dev/spec/Application.js',
    // dns
    '../dns/dnsserver/Application.js',
    '../dns/dnszone/Application.js',
    '../dns/dnszoneprofile/Application.js',
    // fm
    '../fm/alarm/Application.js',
    '../fm/alarmclass/Application.js',
    '../fm/alarmclassconfig/Application.js',
    '../fm/alarmdiagnosticconfig/Application.js',
    '../fm/alarmescalation/Application.js',
    '../fm/alarmseverity/Application.js',
    '../fm/alarmtrigger/Application.js',
    '../fm/classificationrule/Application.js',
    '../fm/event/Application.js',
    '../fm/eventclass/Application.js',
    '../fm/eventtrigger/Application.js',
    '../fm/ignoreeventrule/Application.js',
    '../fm/ignorepattern/Application.js',
    '../fm/mib/Application.js',
    '../fm/mibpreference/Application.js',
    '../fm/oidalias/Application.js',
    '../fm/reportalarmdetail/Application.js',
    '../fm/ttsystem/Application.js',
    // gis
    // '../gis/area/Application.js', // not found in menu
    '../gis/building/Application.js',
    '../gis/division/Application.js',
    '../gis/layer/Application.js',
    // '../gis/overlay/Application.js', // not found in menu
    '../gis/street/Application.js',
    // '../gis/tms/Application.js', // not found in menu
    // inv
    '../inv/allocationgroup/Application.js',
    '../inv/capability/Application.js',
    '../inv/connectionrule/Application.js',
    '../inv/connectiontype/Application.js',
    '../inv/coverage/Application.js',
    '../inv/firmware/Application.js',
    '../inv/firmwarepolicy/Application.js',
    '../inv/interface/Application.js',
    '../inv/interfaceclassificationrule/Application.js',
    '../inv/interfaceprofile/Application.js',
    '../inv/inv/Application.js',
    '../inv/macdb/Application.js',
    '../inv/map/Application.js',
    '../inv/modelinterface/Application.js',
    '../inv/modelmapping/Application.js',
    '../inv/networksegment/Application.js',
    '../inv/networksegmentprofile/Application.js',
    '../inv/objectmodel/Application.js',
    '../inv/platform/Application.js',
    '../inv/reportifacestatus/Application.js',
    '../inv/reportlinkdetail/Application.js',
    '../inv/reportmetrics/Application.js',
    '../inv/resourcegroup/Application.js',
    '../inv/technology/Application.js',
    '../inv/unknownmodel/Application.js',
    '../inv/vendor/Application.js',
    // ip
    '../ip/addressprofile/Application.js',
    '../ip/addressrange/Application.js',
    '../ip/ipam/Application.js',
    '../ip/prefixaccess/Application.js',
    '../ip/prefixprofile/Application.js',
    '../ip/vrf/Application.js',
    '../ip/vrfgroup/Application.js',
    // kb
    '../kb/kbentry/Application.js',
    // main
    '../main/audittrail/Application.js',
    '../main/authldapdomain/Application.js',
    '../main/chpolicy/Application.js',
    // '../main/config/Application.js', // not found in menu
    '../main/crontab/Application.js',
    '../main/customfield/Application.js',
    '../main/customfieldenumgroup/Application.js',
    '../main/desktop/app.js',
    '../main/extstorage/Application.js',
    '../main/handler/Application.js',
    '../main/jsonimport/Application.js',
    '../main/language/Application.js',
    '../main/mimetype/Application.js',
    '../main/notificationgroup/Application.js',
    '../main/pool/Application.js',
    '../main/prefixtable/Application.js',
    '../main/pyrule/Application.js',
    // '../main/ref/Application.js', // not found in menu
    '../main/refbookadmin/Application.js',
    '../main/remotesystem/Application.js',
    '../main/reportsubscription/Application.js',
    '../main/resourcestate/Application.js',
    '../main/search/Application.js',
    '../main/style/Application.js',
    // '../main/sync/Application.js', // not found in menu - deleted
    '../main/systemnotification/Application.js',
    '../main/systemtemplate/Application.js',
    '../main/tag/Application.js',
    '../main/template/Application.js',
    '../main/timepattern/Application.js',
    '../main/userprofile/Application.js',
    '../main/welcome/Application.js',
    // maintenance
    '../maintenance/maintenance/Application.js',
    '../maintenance/maintenancetype/Application.js',
    // peer
    '../peer/as/Application.js',
    '../peer/asprofile/Application.js',
    '../peer/asset/Application.js',
    '../peer/community/Application.js',
    '../peer/communitytype/Application.js',
    '../peer/maintainer/Application.js',
    '../peer/organisation/Application.js',
    '../peer/peer/Application.js',
    '../peer/peergroup/Application.js',
    '../peer/peeringpoint/Application.js',
    '../peer/person/Application.js',
    '../peer/prefixlistbuilder/Application.js',
    '../peer/rir/Application.js',
    // phone
    '../phone/dialplan/Application.js',
    '../phone/numbercategory/Application.js',
    '../phone/phonenumber/Application.js',
    '../phone/phonenumberprofile/Application.js',
    '../phone/phonerange/Application.js',
    '../phone/phonerangeprofile/Application.js',
    // pm
    '../pm/metricscope/Application.js',
    '../pm/metrictype/Application.js',
    '../pm/thresholdprofile/Application.js',
    // project
    '../project/project/Application.js',
    // sa
    '../sa/action/Application.js',
    '../sa/actioncommands/Application.js',
    '../sa/administrativedomain/Application.js',
    '../sa/authprofile/Application.js',
    '../sa/capsprofile/Application.js',
    '../sa/commandsnippet/Application.js',
    '../sa/getnow/Application.js',
    '../sa/groupaccess/Application.js',
    '../sa/managedobject/Application.js',
    '../sa/managedobjectprofile/Application.js',
    '../sa/managedobjectselector/Application.js',
    // '../sa/mrt/Application.js', // not found in menu
    '../sa/objectnotification/Application.js',
    '../sa/profile/Application.js',
    '../sa/profilecheckrule/Application.js',
    '../sa/reportobjectdetail/Application.js',
    '../sa/runcommands/Application.js',
    '../sa/service/Application.js',
    '../sa/serviceprofile/Application.js',
    '../sa/useraccess/Application.js',
    // sla
    '../sla/slaprobe/Application.js',
    '../sla/slaprofile/Application.js',
    // support
    '../support/account/Application.js',
    '../support/crashinfo/Application.js',
    // vc
    '../vc/vc/Application.js',
    '../vc/vcbindfilter/Application.js',
    '../vc/vcdomain/Application.js',
    '../vc/vcfilter/Application.js',
    '../vc/vctype/Application.js',
    '../vc/vlan/Application.js',
    '../vc/vlanprofile/Application.js',
    '../vc/vpn/Application.js',
    '../vc/vpnprofile/Application.js',
    // wf
    '../wf/state/Application.js',
    '../wf/transition/Application.js',
    '../wf/wfmigration/Application.js',
    '../wf/workflow/Application.js',
];

module.exports = apps;
