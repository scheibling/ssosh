from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template


# Create your views here.
def IndexView(request):  
    return HttpResponse(get_template('ssosh_index.html').render({}, request))

def SuccessView(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200, content_type="text/html", content="You have successfully logged in!")
    else:
        return redirect("/oidc")