from django.urls import path
from . import views

urlpatterns = [
    # example: /budget
    path('', views.index, name='index'),
]