from django.urls import re_path
from ssosh_server.oidc_client import views

urlpatterns = [
	re_path(r'^$', views.login, name='login'),
 	re_path(r'^login/admin$', views.login_admin, name='login-admin'),
	re_path(r'^callback/$', views.callback, name='login-callback'),
	re_path(r'^logout/$', views.logout, name='logout'),
]
