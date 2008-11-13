from django.contrib import admin
from noc.peer.models import LIR,AS,ASSet,PeeringPoint,PeerGroup,Peer,LGQueryCommand,CommunityType,Community

class LIRAdmin(admin.ModelAdmin): pass

class ASAdmin(admin.ModelAdmin):
    list_display=["asn","description","lir","rpsl_link"]
    list_filter=["lir"]
    search_fields=["asn","description"]
    
class CommunityTypeAdmin(admin.ModelAdmin):
    list_display=["name"]
    
class CommunityAdmin(admin.ModelAdmin):
    list_display=["community","type","description"]
    list_filter=["type"]
    search_fields=["community","description"]
        
class ASSetAdmin(admin.ModelAdmin):
    list_display=["name","description","members","rpsl_link"]
    search_fields=["name","description","members"]

class LGQueryCommandAdmin(admin.TabularInline):
    model=LGQueryCommand
    extra=1

class PeeringPointAdmin(admin.ModelAdmin):
    list_display=["hostname","location","local_as","router_id","profile_name","communities","rpsl_link"]
    list_filter=["profile_name"]
    search_fields=["hostname","router_id"]
        
class PeerGroupAdmin(admin.ModelAdmin):
    list_display=["name","description","communities"]
        
class PeerAdmin(admin.ModelAdmin):
    list_display=["peering_point","local_asn","remote_asn","admin_import_filter","admin_export_filter","local_ip","masklen","remote_ip","admin_tt_url","description","communities"]
    search_fields=["remote_asn","description"]
    list_filter=["peering_point"]

admin.site.register(LIR,LIRAdmin)
admin.site.register(AS,ASAdmin)
admin.site.register(CommunityType,CommunityTypeAdmin)
admin.site.register(Community,CommunityAdmin)
admin.site.register(ASSet,ASSetAdmin)
admin.site.register(PeeringPoint,PeeringPointAdmin)
admin.site.register(PeerGroup,PeerGroupAdmin)
admin.site.register(Peer,PeerAdmin)