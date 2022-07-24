from django.urls import path
from . import views

urlpatterns = [
    # example: /account/login
    path('login', views.user_login, name='login'),
]