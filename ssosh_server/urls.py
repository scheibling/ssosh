"""ssoshell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
import ssosh_server.interface.views as ssosh_views

admin.site.site_title = "SSO Shell"
admin.site.name = "SSO Shell"
admin.site.site_header = "Administration"
admin.site.index_title = "Administration"

# Host bootstrap flow
# 1. Request to /host/bootstrap/HOSTNAME01 or /host/bootstrap/HOSTNAME01/{id}
# 2. If ID is provided and correct, goto 5.
# 3. Return /auth/init url for user to login (admin)
# 4. Await loop /host/callback
# 5. When user done, /host/callback returns ID, CA, Principals
# 6. Save to config on host, restart sshd

# Client auth flow
# 1. Request to /ssh_ca/auth/
# 2. Return URl to /auth/init for user login
# 3. Await loop /auth/callback
# 4. When user done, /auth/callback returns certificate


urlpatterns = [
    # # / -> empty page
    path('', ssosh_views.IndexView),
    
    # /(login|logout) -> delete session
    path('login', auth_views.LoginView.as_view()),
    path('logout', auth_views.LogoutView.as_view()),
    path('success', ssosh_views.SuccessView),
    
    # /admin/* -> django.admin
    re_path('^admin/', admin.site.urls),
    
    # # /auth/* -> ssosh_server.oidc_client
    re_path(r'^oidc/', include('ssosh_server.oidc_client.urls')),
    
    # # /auth/* -> ssosh_server.oidc_client
    re_path(r'^auth/', include('ssosh_server.device_auth.urls')),
    
    # # /host/* -> ssosh_server.hosts
    # re_path(r'hosts/', include('ssosh_server.hosts.urls'), name='hosts'),
    
    # # /device/* -> ssosh_server.device
    # re_path(r'^device/', include('ssosh_server.device.urls')), 
    
    # # /host/* -> ssosh_server.host
    
    # # /client/* -> ssosh_server.client
    # re_path(r'^client/', include('ssosh_server.client.urls'))
]
# admin.autodiscover()

# urlpatterns = [
#     re_path('^', include('ssosh_server.user.urls')),
#     re_path('^admin/', admin.site.urls),
#     re_path(r'^auth/', include('ssosh_server.oidc_client.urls')),
#     re_path(r'^device/', include('ssosh_server.device_auth.urls')),
#     re_path('^host/', include('ssosh_server.host.urls')),
# ]