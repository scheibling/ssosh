from ssosh_server.device_auth.decorators import device_token_required, host_key_required
from datetime import datetime, timedelta
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from ssosh_server.device_auth.models import DeviceAuthRequest, DeviceAccessToken
from django.contrib.auth.models import User
from ssosh_server.hosts.models import Host

@csrf_exempt
@device_token_required('host.bootstrap')
def bootstrap(request: WSGIRequest, user: User):
    if request.method != 'POST':
        return HttpResponseNotAllowed(f'Invalid request method ({request.method})')

    hostname = request.POST.get('hostname', None).upper()
    
    if not hostname:
        return HttpResponseBadRequest('Invalid hostname')

    try:
        host: Host = Host.objects.get(hostname=hostname)
    except Host.DoesNotExist:
        host = Host(
            hostname=hostname
        )
        host.save()

    return JsonResponse(
        host.get_host_config()
    )
    
@csrf_exempt
@host_key_required()
def config(request: WSGIRequest, hostname: str, host: Host):
    hostname = hostname.upper()
    if host.hostname != hostname:
        return HttpResponseBadRequest('Invalid hostname or token')
        
    return JsonResponse(
        host.get_host_config()
    )