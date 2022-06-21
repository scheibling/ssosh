from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.http.response import HttpResponseForbidden
from ssosh_server.device_auth.models import DeviceAccessToken
from django.core.handlers.wsgi import WSGIRequest


def device_token_required(admin: bool = False):
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

            if admin and not token.is_admin:
                return HttpResponseForbidden('You do not have the privilege to perform this operation')
            
            if token.expires < datetime.now(tz=token.expires.tzinfo):
                return HttpResponseForbidden('Token expired')

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