from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return HttpResponse("budget. You are logged in")
    else:
        return HttpResponseRedirect('/accounts/login')