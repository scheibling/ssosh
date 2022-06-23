# hosts/urls.py
from django.urls import path
from ssosh_server.client import views as client_views

urlpatterns = [
    # Require token authentication
    # Adds client to user
    # path("^bootstrap$", client_views.bootstrap, name="client_bootstrap"),
    
    # Deauthorize client
    path("deauthorize/<str:ident>", client_views.deauthorize, name="client_deauthorize"),
    
    # Token auth
    path("certificate", client_views.issue_certificate, name="get_cert"),

    # path("^config$", client_views.config, name="auth_config"),

    # path("^device/callback$", auth_views.callback, name="auth_device_callback"),
    # path("^principals$", auth_views.get_principals, name="auth_principals"),
    # path("^ca_pubkey$", auth_views.get_certificate, name="auth_ca_pubkey")
]