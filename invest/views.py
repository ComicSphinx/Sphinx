from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# возможно, тут надо сделать @login_required вместо if user authenticated
def index(request):
    if request.user.is_authenticated:
        return HttpResponse("invest. You are logged in")
    else:
        return HttpResponseRedirect('/account/login')