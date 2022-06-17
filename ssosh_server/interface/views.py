from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def IndexView(request):  
    return HttpResponse(status=200, content_type="text/html", content='#')

def SuccessView(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200, content_type="text/html", content="You have successfully logged in!")
    else:
        return redirect("/oidc")