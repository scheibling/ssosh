from threading import Lock
from django.conf import settings
from openid_connect import connect
from importlib import import_module
from datetime import datetime, timedelta
from django.core.exceptions import ImproperlyConfigured

OIDC_SERVER_CACHE = None
OIDC_CACHE_LOCK = Lock()
OIDC_CACHE_EXPIRES = 0

def get_op_connection():
    global OIDC_SERVER_CACHE, OIDC_CACHE_LOCK, OIDC_CACHE_EXPIRES
    
    if None in [
                getattr(settings, 'OIDC_AUTH_SERVER', None),
                getattr(settings, 'OIDC_AUTH_CLIENT_ID', None),
                getattr(settings, 'OIDC_AUTH_CLIENT_SECRET', None),
            ]:
        raise ImproperlyConfigured(
            "OIDC_AUTH_SERVER, OIDC_AUTH_CLIENT_ID, and " +
            "OIDC_AUTH_CLIENT_SECRET must be set in settings.py to use OIDC"
        )
    
    with OIDC_CACHE_LOCK:
        now = datetime.now()
        
        if not OIDC_CACHE_EXPIRES or OIDC_CACHE_EXPIRES <= now.timestamp():
            OIDC_SERVER_CACHE = connect(
                server=settings.OIDC_AUTH_SERVER,
                client_id=settings.OIDC_AUTH_CLIENT_ID,
                client_secret=settings.OIDC_AUTH_CLIENT_SECRET,
                protocol=getattr(settings, 'OIDC_AUTH_PROTOCOL', None)
            )
            
            OIDC_CACHE_EXPIRES = (now + timedelta(hours=1)).timestamp()
            
        return OIDC_SERVER_CACHE
    
def _import_object(path, def_name):
	try:
		mod, cls = path.split(':', 1)
	except ValueError:
		mod = path
		cls = def_name

	return getattr(import_module(mod), cls)