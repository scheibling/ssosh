from secrets import token_urlsafe
from datetime import datetime, timedelta
from uuid import uuid4 as gen_uuid
from django.db import models
from django.contrib.auth.models import User

class DeviceAuthRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid(), editable=False)
    code = models.CharField(max_length=120, default=token_urlsafe(16), unique=True, blank=False)
    time = models.DateTimeField()
    expires = models.DateTimeField()
    metadata = models.JSONField()
    completed = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(DeviceAuthRequest, self).__init__(*args, **kwargs)
        if self.time is None:
            self.time = datetime.now()
        if self.expires is None:
            self.expires = self.time + timedelta(minutes=10)

    def getResponse(
        self, 
        auth_url,
        callback_url,
        interval: int = 5, 
    ):
        return {
            'auth_url': auth_url,
            'callback_url': callback_url,
            'code': self.code,
            'exp': int(self.expires.timestamp()),
            'int': interval
        }

class DeviceAccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid(), editable=False)
    code = models.CharField(max_length=120, unique=True, blank=False)
    token = models.CharField(max_length=120, default=token_urlsafe(32), unique=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_admin = models.BooleanField(default=False)
    time = models.DateTimeField()
    expires = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(DeviceAccessToken, self).__init__(*args, **kwargs)
        if self.time is None:
            self.time = datetime.now()
        if self.expires is None:
            self.expires = self.time + timedelta(minutes=30)

    def getResponse(self):
        return {
            'token': self.token,
            'exp': int(self.expires.timestamp())
        }