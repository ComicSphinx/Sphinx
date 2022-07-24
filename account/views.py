from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate, login
from account.forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(username=credentials['login'], password=credentials['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Успешно авторизован')
                else:
                    return HttpResponse("Не активный аккаунт")
            else:
                return HttpResponse("Введены некорретные  данные")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})