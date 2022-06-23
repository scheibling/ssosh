from sshkey_tools.keys import PublicKey
from django.contrib.auth.models import User
from ssosh_server.hosts.models import Hostgroup

def is_valid_pubkey(pubkey: str) -> bool:
    try:
        PublicKey.from_string(pubkey)
        return True
    except Exception:
        return False
    
def get_user_principals(user: User) -> str:
    principals = [
        user.username
    ]
    
    for grp in user.groups.all():
        principals.append(f"grp_{grp.name}")
        
    for hgr in Hostgroup.objects.filter(userlink__id__contains=user.id):
        principals.append(f"hgr_{hgr.slug}")

    return principals