from django.db import models
from django.conf import settings
from django.urls import reverse
from uuid import uuid4 as gen_uuid
from secrets import token_urlsafe
from django.contrib.auth.models import User


def token_32bit():
    return token_urlsafe(32)

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False, verbose_name='ID')
    hostname = models.CharField(max_length=255, verbose_name='Hostname')
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address')
    key = models.CharField(max_length=100, default=token_32bit, verbose_name="Auth key")
    userlink = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Owner')
    active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    def __str__(self):
        return f"{self.hostname} ({self.ip}) - {self.userlink.username}"
    
    def get_client_config(self) -> str:
        return {
            'hostname': self.hostname,
            'key': self.key,
            'base_url': settings.BASE_URL,
            'ca_pubkey': settings.SSH_CA.public_key.to_string()
        }