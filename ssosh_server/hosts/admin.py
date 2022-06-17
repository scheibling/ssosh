from django.contrib import admin
from ssosh_server.hosts.models import (
    Host,
    Hostgroup,
    LnkHostToHostgroup,
    LnkUserToHost,
    LnkUserToHostgroup,
    LnkGroupToHost,
    LnkGroupToHostgroup,
)

class HostHostgroupLinkInline(admin.TabularInline):
    model = LnkHostToHostgroup
    fields=['host', 'group']
    extra = 0
    
class UserHostLinkInline(admin.TabularInline):
    model = LnkUserToHost
    fields=['host', 'user']
    extra = 0
    
class UserHostgroupLinkInline(admin.TabularInline):
    model = LnkUserToHostgroup
    fields=['user', 'hostgroup']
    extra = 0

class GroupHostLinkInline(admin.TabularInline):
    model = LnkGroupToHost
    fields=['host', 'group']
    extra = 0
    
class GroupHostgroupLinkInline(admin.TabularInline):
    model = LnkGroupToHostgroup
    fields=['hostgroup', 'group']
    extra = 0
    
class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Enter the hostname for the server", {'fields': ['hostname']}),
    ]

    list_display = ['hostname']
    readonly_fields = ['id']
    inlines = [
        HostHostgroupLinkInline,
        UserHostLinkInline,
        GroupHostLinkInline
    ]
    
class HostgroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Enter a name for your host group', {'fields': ('name',)}),
        ('Enter a slug for your group name (a-zA-Z0-9\-\_)', {'fields': ('slug',)})
    )
    list_display = ('name', 'slug')
    readonly_fields = ['id']
    inlines = [
        HostHostgroupLinkInline,
        UserHostgroupLinkInline,
        GroupHostgroupLinkInline
    ]

admin.site.register(Host, HostAdmin)
admin.site.register(Hostgroup, HostgroupAdmin)

