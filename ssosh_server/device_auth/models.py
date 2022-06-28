from secrets import token_urlsafe
from datetime import datetime, timedelta
from django.utils import timezone
from uuid import uuid4 as gen_uuid
from django.db import models
from django.contrib.auth.models import User

def token_32bit():
    return token_urlsafe(32)

class DeviceAuthRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    code = models.CharField(max_length=120, default=token_32bit, unique=True, blank=False)
    time = models.DateTimeField()
    expires = models.DateTimeField()
    metadata = models.JSONField()
    scopes = models.CharField(max_length=255, blank=False)
    completed = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(DeviceAuthRequest, self).__init__(*args, **kwargs)
        if self.time is None:
            self.time = timezone.now()
        if self.expires is None:
            self.expires = self.time + timezone.timedelta(minutes=10)

    def getResponse(
        self, 
        auth_url,
        callback_url,
        interval: int = 1, 
    ):
        return {
            'auth_url': f"{auth_url}?code={self.code}",
            'callback_url': f"{callback_url}?code={self.code}",
            'exp': int(self.expires.timestamp()),
            'int': interval
        }

class DeviceAccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    code = models.CharField(max_length=120, unique=True, blank=False)
    token = models.CharField(max_length=120, default=token_32bit, unique=True, blank=False)
    scopes = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_admin = models.BooleanField(default=False)
    time = models.DateTimeField()
    expires = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(DeviceAccessToken, self).__init__(*args, **kwargs)
        if self.time is None:
            self.time = timezone.now()
        if self.expires is None:
            self.expires = self.time + timezone.timedelta(hours=100)

    def getResponse(self):
        return {
            'scopes': [scope for scope in self.scopes.split(',')],
            'token': self.token,
            'exp': int(self.expires.timestamp())
        }