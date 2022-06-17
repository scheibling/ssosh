from time import time
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, resolve_url
from django.core.exceptions import ImproperlyConfigured
from ssosh_server.exceptions import LoginRedirectLoop
from ssosh_server.oidc_client.auth import get_op_connection, _import_object

USR_LOGIN_REDIRECT_PATH = getattr(settings, 'USR_LOGIN_REDIRECT_PATH', '/success')
ADM_LOGIN_REDIRECT_PATH = getattr(settings, 'ADM_LOGIN_REDIRECT_PATH', '/admin/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

AUTH_SCOPE = getattr(settings, 'OIDC_AUTH_SCOPE', ('openid'))
ALLOWED_REDIRECTION_HOSTS = getattr(
    settings, 'OIDC_ALLOWED_REDIRECTION_HOSTS', ''
).split(',')

USERINFO_ATTRIBUTE_MATCH = getattr(settings, 'OIDC_USERINFO_ATTRIBUTE_MATCH', {
    "email": "email",
    "displayname": "displayname",
    "given_name": "given_name",
    "surname": "surname"
})

try:
    user_match = getattr(
        settings, 'OIDC_USER_MATCH_FUNCTION', 'django_auth_oidc:get_user_by_username'
    )
    USER_MATCH_FUNCTION = _import_object(user_match, 'get_user')
except ImportError:
    raise ImproperlyConfigured(
        f"The specified OIDC_USER_MATCH_FUNCTION {user_match} could not be imported. " +
        "Make sure it exists and is installed."
    ) from ImportError
    

def login(request: WSGIRequest, return_path: str = USR_LOGIN_REDIRECT_PATH):
    """
    Check if the user is already authenticated, and if the session
    is still valid. If not, initiate new authentication.
    """
    request.session['LOGIN_LOOP'] = request.session.get('LOGIN_LOOP', 0) + 1
    if request.session['LOGIN_LOOP'] > 5:
        request.session.pop('LOGIN_LOOP')
        raise LoginRedirectLoop(
            "Login redirect loop detected. Please check your OP configuration."
        )
    request.session['RETURN_PATH'] = return_path
    if request.user.is_authenticated or (
        request.session.get('oidc_id', False) and
        request.session.get('oidc_id', {}).get('exp', 0) < time()
    ):
        return redirect(resolve_url(return_path))
    
    return redirect(
        get_op_connection().authorize(
            redirect_uri = request.build_absolute_uri(
                reverse("login-callback")
            )
        )
    )

def login_admin(request: WSGIRequest):
    return login(request, ADM_LOGIN_REDIRECT_PATH)

def callback(request: WSGIRequest):
    state = request.GET.get("state", None)
    code = request.GET.get("code", None)
    
    if not code:
        return login(request, request.session.get(
            'RETURN_PATH', USR_LOGIN_REDIRECT_PATH
        ))
     
    op = get_op_connection()
        
    token = op.request_token(
        redirect_uri=request.build_absolute_uri(
            reverse("login-callback")
        ),
        code=code
    )
    
    user = USER_MATCH_FUNCTION(token.id)
    if not user or not user.is_authenticated:
        return login(request, request.session.get(
            'RETURN_PATH', USR_LOGIN_REDIRECT_PATH
        ))
    
    userinfo = op.get_userinfo(token.access_token)
    
    auth.login(request, user)
    current_user = auth.get_user(request)
    
    for local, oidc in USERINFO_ATTRIBUTE_MATCH.items():
        if userinfo.get(oidc):
            setattr(current_user, local, userinfo[oidc])
        
    current_user.save()
    request.session['oidc_id_token'] = token.id_token
    request.session['oidc_id'] = token.id
    request.session['oidc_state'] = state
    
    request.session.pop('LOGIN_LOOP')
    return redirect(request.session.pop('RETURN_PATH'))

def logout(request: WSGIRequest):
    auth.logout(request)
    oidc_op = get_op_connection()
    request.session.pop('oidc_id', None)
    
    logout_url = request.build_absolute_uri(
        LOGOUT_REDIRECT_URL
    )
    
    if oidc_op.end_session_endpoint:
        return redirect(oidc_op.end_session(
            post_logout_redirect_uri=logout_url,
            state=request.session.pop('oidc_state', None),
            id_token_hint = request.session.pop('oidc_id_token', None)
        ))
    else:
        return redirect(logout_url)