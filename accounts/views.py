from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, ChangePasswordForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/budget')
    else: 
        form = LoginForm()

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        username = request.user.username
        new_password = request.POST['password']
        User.objects.get(username=username).set_password(new_password)
        return HttpResponse("Пароль изменен успешно")
    else:
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {'form': form})