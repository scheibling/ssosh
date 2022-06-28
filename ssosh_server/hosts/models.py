import json
from django.db import models
from django.conf import settings
from django.urls import reverse
from secrets import token_urlsafe
from django.db.models.manager import EmptyManager
from uuid import uuid4 as gen_uuid
from django.contrib.auth.models import User, Group

def token_32bit():
    return token_urlsafe(32)

# Ensure all hostnames are stored in upper case
class UpperCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
            super(UpperCaseCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)

class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hostname = UpperCaseCharField(max_length=255)
    key = models.CharField(max_length=100, default=token_32bit)
    hostgrouplink = models.ManyToManyField("Hostgroup", 'host_hostgroup_link', verbose_name="Hostgroups", blank=True)
    userlink = models.ManyToManyField(User, 'host_user_link', verbose_name="Users", blank=True)
    grouplink = models.ManyToManyField(Group, 'host_group_link', verbose_name="Groups", blank=True)
    
    class Meta:
        verbose_name = "Host"
        # The space is used for quick and dirty sorting in the admin sidebar
        # It is not rendered in the UI
        verbose_name_plural = " Hosts"

    def __str__(self):
        return str(self.hostname)
    
    def get_allowed_principals(self) -> list:
        principals = []
        
        for hostgroup in self.hostgrouplink.all():
            principals.append(f'hgr_{hostgroup.slug}')
            
        for user in self.userlink.all():
            principals.append(f'usr_{user.username}')
            
        for group in self.grouplink.all():
            principals.append(f'grp_{group.name}')
            
        return principals
    
    def get_host_config(self) -> str:
        return {
            'hostname': str(self.hostname),
            'config_url': settings.BASE_URL + reverse('host_config', kwargs={"hostname": self.hostname}),
            'principals': self.get_allowed_principals(),
            'ca_pubkey': settings.SSH_CA.public_key.to_string(),
            'key': str(self.key),
            'interval': settings.HOST_REFRESH_INTERVAL
        }
        
        

class Hostgroup(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=128, unique=True, blank=False, null=False, verbose_name="Slug (a-zA-Z0-9\-\_)")
    hostlink = models.ManyToManyField(Host, 'hostgroup_host_link', verbose_name="Hosts", through="Host_hostgrouplink", blank=True)
    userlink = models.ManyToManyField(User, 'hostgroup_user_link', verbose_name="Users", blank=True)
    grouplink = models.ManyToManyField(Group, 'hostgroup_group_link', verbose_name="Groups", blank=True)

    class Meta:
        verbose_name = "Hostgroup"
        verbose_name_plural = "Hostgroups"

    def __str__(self):
        return str(self.name)