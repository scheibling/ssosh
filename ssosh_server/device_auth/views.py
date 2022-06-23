from datetime import datetime, timedelta
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from ssosh_server.device_auth.models import DeviceAuthRequest, DeviceAccessToken

@csrf_exempt
def auth_init_device(request: WSGIRequest):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Invalid request method')

    if not (scopes := request.POST.get('scopes', None)):
        return HttpResponseBadRequest('Invalid or no scopes requested')
    
    for scope in scopes.split(','):
        if scope not in settings.SSH_CA_SCOPES.keys():
            return HttpResponseBadRequest('Invalid or no scopes requested')
    
    auth_request = DeviceAuthRequest(
        scopes=scopes,
        metadata = json.dumps({
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'host': request.META.get('HTTP_HOST')
        })
    )

    auth_request.save()

    return JsonResponse(
        auth_request.getResponse(
            auth_url = request.build_absolute_uri(reverse('auth_init')),
            callback_url = request.build_absolute_uri(reverse('auth_callback'))
        )
    )

@login_required(login_url='/login')
def authenticate(request: WSGIRequest):
    if not request.method == 'GET':
        return HttpResponseBadRequest('Invalid authentication request')

    # Get auth request data
    auth_request = DeviceAuthRequest.objects.filter(
        code=request.GET.get('code')
    ).first()

    if not auth_request or auth_request.completed:
        return HttpResponseBadRequest('Invalid authentication request')

    for scope in auth_request.scopes.split(','):
        if scope not in settings.SSH_CA_SCOPES.keys():
            return HttpResponseBadRequest('Invalid or no scopes requested')

    if request.user.is_authenticated:
        scopes = auth_request.scopes.split(',')
        for scope in scopes:
            required_perms = settings.SSH_CA_SCOPES.get(scope, None)
            if (
            ( required_perms['requires_admin'] and not request.user.is_superuser ) or
            ( required_perms['requires_staff'] and not request.user.is_staff )
            ):
                return HttpResponseNotAllowed('You do not have permission to access this scope')
        
        
        auth_request.completed = True
        auth_request.save()
        
        token = DeviceAccessToken(
            code = str(auth_request.code),
            scopes=auth_request.scopes,
            user=request.user,
            is_admin = request.user.is_superuser
        )

        token.save()

        return HttpResponse(get_template('success.html').render({}, request))

    return HttpResponseBadRequest('Invalid authentication request')

@csrf_exempt
def callback(request: WSGIRequest):
    if not request.method == 'GET':
        return HttpResponseBadRequest('Invalid request method')

    # Get auth request data
    auth_request: DeviceAuthRequest = DeviceAuthRequest.objects.filter(
        code=request.GET.get('code')
    ).first()

    if not auth_request:
        return HttpResponseBadRequest('The provided code is incorrect')

    if auth_request.completed:
        token: DeviceAccessToken = DeviceAccessToken.objects.filter(
            code=auth_request.code
        ).first()

        if not token:
            return HttpResponseBadRequest('The authentication attempt was unsuccessful. Please try again.')
        
        return JsonResponse(token.getResponse())