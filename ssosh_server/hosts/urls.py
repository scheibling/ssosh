# hosts/urls.py
from django.urls import path, re_path
from ssosh_server.hosts import views as host_views

urlpatterns = [
    re_path(r"^bootstrap/?", host_views.bootstrap, name="host_bootstrap"),
    re_path(r"^config/(?P<hostname>[a-zA-Z0-9-]+)/?", host_views.config, name="host_config")
]