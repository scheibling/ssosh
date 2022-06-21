# hosts/urls.py
from django.urls import path, re_path
from ssosh_server.device_auth import views as auth_views

urlpatterns = [
    re_path(r'^device/?', auth_views.auth_init_device, name='auth_init_device'),
    re_path(r'^authenticate/?', auth_views.authenticate, name='auth_init'),
    re_path(r'^callback/?', auth_views.callback, name='auth_callback')
]