from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate, login
from account.forms import LoginForm

def user_login(request):
    return ''