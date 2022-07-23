from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return HttpResponse("invest. You are logged in")
    else:
        # TODO редирект на страницу авторизации
        return HttpResponse("you are not logged in")
