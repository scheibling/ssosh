from django.contrib import admin
from ssosh_server.client.models import Device

# Not exactly best practice design-wise, but we want the device list to be filtered
# on active status by default to minimize clutter.
class ActiveDeviceFilter(admin.SimpleListFilter):
    title='Show only active devices'
    parameter_name='active'
    
    def lookups(self, request, model_admin):
        return (
            ('Active', 'Show active devices'),
            ('Inactive', 'Show inactive devices'),
            ('All', 'Show all devices')
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'Inactive':
            return queryset.filter(active=False)

        if self.value() == 'All':
            return queryset
                
        return queryset.filter(active=True)
            

class DeviceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Device Information", {
            "fields": (
                "id",
                "hostname",
                "ip",
                "key",
                "userlink",
                "active"
            )
        })
    ]

    list_display = ['hostname', 'ip', 'userlink', 'active']
    list_filter = [ ActiveDeviceFilter ]

    # readonly_fields = ['id', 'hostname', 'ip', 'key', 'userlink', 'active']
    readonly_fields = ['id']
    actions = ['deauthorize']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not request.user.is_superuser:
            queryset = queryset.filter(userlink_id__exact=request.user.id)
        return queryset, use_distinct
    
    def has_module_permission(self, request) -> bool:
        return True
    
    def has_view_permission(self, request, obj=None) -> bool:
        return True
    
    @admin.action(description='Deauthorize device', permissions=['view'])
    def deauthorize(modeladmin, request, queryset):
        print("Hello")
        return True

admin.site.register(Device, DeviceAdmin)

