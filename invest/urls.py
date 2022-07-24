from django.urls import path
from . import views

urlpatterns = [
    # example: /invest
    path('', views.index, name='index'),
]