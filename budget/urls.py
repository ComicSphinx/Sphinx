from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_view, name='budget_view')
]