from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, ChangePasswordForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/accounts/profile')
            else: # TODO Возвращать ошибку о некорректном пароле или логине
                return render(request, 'login.html', {'form': form})        
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/profile')

def registration_view(request):
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
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='/accounts/login/')
def change_password_view(request): # TODO оно не работает (не меняет пароль, хотя возвращает успешный response). Возможно, я не сохраняю?
    if request.method == 'POST':
        username = request.user.username
        new_password = request.POST['password']
        
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        
        return HttpResponse("Пароль изменен успешно")
    else:
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {'form': form})