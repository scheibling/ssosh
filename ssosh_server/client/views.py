from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4 as gen_uuid
from django.contrib.auth.models import User
from ssosh_server.client.models import Device
from ssosh_server.device_auth.decorators import device_key_required, device_token_required
from ssosh_server.authority.models import SSHCertificate, CertTypes
from ssosh_server.authority.utils import is_valid_pubkey, get_user_principals
from django.utils import timezone

@csrf_exempt
@device_token_required('client.bootstrap')
def bootstrap(request: WSGIRequest, user: User):
    if request.method != 'POST':
        return HttpResponseNotAllowed(f'Invalid request method ({request.method})')

    hostname = request.POST.get('hostname', None)
    
    if not hostname:
        return HttpResponseBadRequest('Invalid hostname')

    hostname = hostname.upper()

    try:
        device: Device = Device.objects.get(hostname=hostname, userlink=user)
    except Device.DoesNotExist:
        device = Device(
            hostname=hostname,
            ip=request.META.get('REMOTE_ADDR'),
            userlink=user,
        )
        device.save()

    return JsonResponse(
        device.get_client_config()
    )
    
@csrf_exempt
@device_key_required()
def config(request: WSGIRequest, device: Device):
    if device.ip != request.META.get('REMOTE_ADDR'):
        device.ip = request.META.get('REMOTE_ADDR')
        device.save()

    return JsonResponse(
        device.get_client_config()
    )


@csrf_exempt
@device_key_required()
@device_token_required('client.certificate')
def issue_certificate(request: WSGIRequest, device: Device, user: User):
    if not is_valid_pubkey(request.body):
        return HttpResponseBadRequest('Invalid public key')

    cert = SSHCertificate(
        public_key=request.body,
        key_id = f"{getattr(request.user, settings.SSH_CA_KEYID_IDENTIFIER)}-{gen_uuid()}",
        cert_type = CertTypes.USER,
        principals=','.join(get_user_principals(user)),
        valid_after= timezone.now(),
        valid_before= timezone.now() + timezone.timedelta(**settings.SSH_CA_DEFAULT_VALIDITY),
        requested_by=user,
        requested_from=device
    )
    cert.save()

    return HttpResponse(cert.create_certificate(settings.SSH_CA))

def deauthorize(request: WSGIRequest, ident: str):
    device = Device.objects.get(id=ident)
    
    if (
        device and 
        (
            device.userlink.id == request.user.id or
            request.user.is_superuser
        )
    ):        
        if request.method == 'POST':
            device.active = False
            device.save()
            
            return redirect('/admin/client/device')

        return render(request, 'admin/confirm_deauth.html', context={'device': device})        

    return HttpResponseBadRequest('Invalid request')