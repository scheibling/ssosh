# users/urls.py
from django.urls import path, re_path
from . import views


# URLS
# POST /device/auth/[action]
# Initiate the authentication from the client device
"""
Param:
    action=
    - certificate: (any)
      user_pubkey
    - bootstrap_client: (any)
      none
    - bootstrap_host: (admin)
      hostname
      hostkeys
Response:
    {
        "auth_token": [token],
        "auth_uri": "https://ssosh.company.com/device/init/[token]"
    }
"""

# GET /device/init
# Initiate the authentication for the user
"""
Param:
    auth_token=[token]
Response:
    302 Found -> /auth/
"""


# GET /device/finalize
# Display success message
"""
Param:
    none
Response:
    200 OK Successfully authenticated
"""


# GET /device/callback/[token]
# Returns data to client device
"""
auth_token=[token]

Return:
    200 OK {"success": false}
    200 OK {"success": true}
"""

urlpatterns = [
    re_path(
        r'^auth/<slug:action>', 
        views.start,
        name="auth"
    ),
    re_path(
        r'^init/<slug:', 
        views.init,
        name="init"
    ),
    re_path(
        r'^finalize', 
        views.finalize,
        name="finalize"
    ),
    re_path(
        r'^callback/<slug:token>', 
        views.callback,
        name="callback"
    )
]
