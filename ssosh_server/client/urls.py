# hosts/urls.py
from django.urls import path
from ssosh_server.client import views as client_views

urlpatterns = [
    # No auth
    # No param
    # Returns device auth url
    path("^bootstrap$", client_views.bootstrap, name="client_bootstrap"),
    path("^cert/init$", client_views.bootstrap, name="cert_init"),

    # Token auth
    path("^config$", client_views.config, name="auth_config"),
    path("^cert/get$", client_views.get_certificate, name="get_cert"),

    # path("^device/callback$", auth_views.callback, name="auth_device_callback"),
    # path("^principals$", auth_views.get_principals, name="auth_principals"),
    # path("^ca_pubkey$", auth_views.get_certificate, name="auth_ca_pubkey")
]