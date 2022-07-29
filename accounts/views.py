from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, RegistrationForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('Successful')
    else: 
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    logout(request)
    return HttpResponse('logout')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            return HttpResponse('user created successful')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration.html', {'form': form})


def change_password(request):
    username = request.user.username
    new_password = request.POST['password']
    User.objects.get(username=username).set_password(new_password)
