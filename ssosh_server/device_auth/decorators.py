from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.http.response import HttpResponseForbidden
from ssosh_server.device_auth.models import DeviceAccessToken
from ssosh_server.hosts.models import Host
from ssosh_server.client.models import Device
from django.core.handlers.wsgi import WSGIRequest


def device_token_required(req_scope: str):
    def decorator(view_func):
        def wrap(request: WSGIRequest, *args, **kwargs):
            token_header = request.headers.get('Authorization', None)
            
            if not token_header:
                return HttpResponseForbidden('Invalid authentication parameters')

            if "Bearer" in token_header:
                token_header = token_header.split(" ")[1]

            token: DeviceAccessToken = DeviceAccessToken.objects.filter(token=token_header).first()

            if not token:
                return HttpResponseForbidden('Invalid authentication parameters')
            
            if token.expires < datetime.now(tz=token.expires.tzinfo):
                return HttpResponseForbidden('Token expired')
            
            if req_scope not in token.scopes.split(','):
                return HttpResponseForbidden('Invalid token scope')

            kwargs['user'] = token.user

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator

def host_key_required():
    def decorator(view_func):
        def wrap(request: WSGIRequest, *args, **kwargs):
            hostkey = request.headers.get('X-Host-Key', None)
            
            if not hostkey:
                return HttpResponseForbidden('Invalid authentication parameters')
                
            try:
                host = Host.objects.get(key=hostkey)
            except Host.DoesNotExist:
                return HttpResponseForbidden('Invalid authentication parameters')
            
            kwargs['host'] = host            
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator

def device_key_required():
    def decorator(view_func):
        def wrap(request: WSGIRequest, *args, **kwargs):
            devicekey = request.headers.get('X-Device-Key', None)
            
            if not devicekey:
                return HttpResponseForbidden('Invalid authentication parameters')
                
            try:
                device: Device = Device.objects.get(key=devicekey)
            except Host.DoesNotExist:
                return HttpResponseForbidden('Invalid authentication parameters')
            
            if not device.active:
                return HttpResponseForbidden('This device is not authorized. Please repeat the bootstrap process.')

            kwargs['device'] = device
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator

# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         def wrap(request, *args, **kwargs):
#             if request.user.profile.userStatus in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return render(request, "dashboard/404.html")
#         return wrap
#     return decorator


# def admin_only(view_func):
#     def wrap(request, *args, **kwargs):
#         if request.user.profile.userStatus == "admin":
#             return view_func(request, *args, **kwargs)
#         else:
#             return render(request, "dashboard/404.html")
#     return wrap