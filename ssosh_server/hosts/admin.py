from django.contrib import admin
from ssosh_server.hosts.models import (
    Host,
    Hostgroup,
)

class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Host Settings", {
            "fields": (
                "id",
                "hostname",
                "key"
            )
        }),
        ("Hostgroups", {
            "fields": (
                "hostgrouplink",
            )
        }),
        ("Individual permissions", {
            "fields": (
                "userlink",
                "grouplink"
            )
        })
    ]

    list_display = ['hostname']
    readonly_fields = ['id', 'key']
    filter_horizontal = ['userlink', "grouplink", "hostgrouplink"]

class HostgroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hostgroup Settings", {
            "fields": (
                "id",
                "name",
                "slug"
            )
        }),
        ("Hosts", {
            "fields": (
                "hostlink",
            )
        }),
        ("Individual permissions", {
            "fields": (
                "userlink",
                "grouplink"
            )
        })
    )
    list_display = ('name', 'slug')
    filter_horizontal = ['hostlink', 'userlink', 'grouplink']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'slug']
        else:
            return ['id']

admin.site.register(Host, HostAdmin)
admin.site.register(Hostgroup, HostgroupAdmin)