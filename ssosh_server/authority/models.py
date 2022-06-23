from django.db import models
from secrets import token_urlsafe
from django.db.models.manager import EmptyManager
from uuid import uuid4 as gen_uuid
from django.conf import settings
from django.contrib.auth.models import User, Group
from ssosh_server.client.models import Device
from sshkey_tools.fields import CERT_TYPE
from sshkey_tools.keys import PrivateKey, PublicKey
from sshkey_tools.cert import SSHCertificate as Certificate
from django.utils import timezone

def get_default_validity():
    return timezone.now() + timezone.timedelta(**settings.SSH_CA_DEFAULT_VALIDITY)

class CertTypes(models.IntegerChoices):
    USER = 1
    HOST = 2

class SSHCertificate(models.Model):
    id = models.BigAutoField(primary_key=True)
    key_id = models.TextField(unique=True)
    public_key = models.TextField(null=False, blank=False, unique=False)
    cert_type = models.IntegerField(choices=CertTypes.choices)
    principals = models.TextField(null=False, blank=False)
    valid_after = models.DateTimeField(null=False, blank=False, default=timezone.now)
    valid_before = models.DateTimeField(null=False, blank=False, default=get_default_validity)
    critical = models.TextField(null=True, blank=True, default=','.join(settings.SSH_CA_DEFAULT_CRITICAL_OPTIONS))
    extensions = models.TextField(null=True, blank=False, default=','.join(settings.SSH_CA_DEFAULT_EXTENSIONS))
    signature = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    requested_from = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    requested_at = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False)
    
    def create_certificate(self, private_key: PrivateKey):        
        certificate = Certificate.from_public_class(
            public_key=PublicKey.from_string(self.public_key),
            ca_privkey=private_key,
            key_id=self.key_id,
            serial=self.id,
            cert_type=self.cert_type,
            principals=self.principals.split(',') if self.principals != '' else [],
            valid_after=self.valid_after,
            valid_before=self.valid_before,
            critical_options=self.critical.split(',') if self.critical != '' else [],
            extensions=self.extensions.split(',') if self.extensions != '' else []
        )

        if certificate.can_sign():
            certificate.sign()
            self.signature = certificate.to_string()
            self.signed = True
            self.save()

            return self.signature
        
        raise Exception('Could not sign certificate')