from django.db import models
from uuid import uuid4 as gen_uuid
from django.contrib.auth.models import User, Group

class UUIDPrimaryKeyField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.pop('max_length', None)
        kwargs.pop('primary_key', None)
        super(UUIDPrimaryKeyField, self).__init__(
            *args, 
            primary_key=True,
            max_length=36,
            default=str(gen_uuid()),
            **kwargs
        )

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
    id = UUIDPrimaryKeyField()
    hostname = UpperCaseCharField(max_length=255)
    key = models.CharField(max_length=100,default=str(gen_uuid()))
    
    def __str__(self):
        return self.hostname
    
class Hostgroup(models.Model):
    id = UUIDPrimaryKeyField()
    name = models.CharField(max_length=255)
    slug = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    
    def __str__(self):
        return self.name
    
class LnkHostToHostgroup(models.Model):
    id = UUIDPrimaryKeyField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    group = models.ForeignKey(Hostgroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.host} is assigned to {self.group}"
    
class LnkUserToHost(models.Model):
    id = UUIDPrimaryKeyField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User {self.user} has permissions to {self.host}"
    
class LnkGroupToHost(models.Model):
    id = UUIDPrimaryKeyField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Group {self.group} has permissions to {self.host}"
    
class LnkUserToHostgroup(models.Model):
    id = UUIDPrimaryKeyField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostgroup = models.ForeignKey(Hostgroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User {self.user} has permissions to {self.hostgroup}"
    
class LnkGroupToHostgroup(models.Model):
    id = UUIDPrimaryKeyField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    hostgroup = models.ForeignKey(Hostgroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Group {self.group} has permissions to {self.hostgroup}"
    