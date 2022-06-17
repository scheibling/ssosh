from django import template
register = template.Library()

def get_auth_uri(request):
    if 'admin/login' in request.path:
        return request.build_absolute_uri('/oidc/login/admin')
    return request.build_absolute_uri('/oidc/')

register.filter('get_auth_uri', get_auth_uri)