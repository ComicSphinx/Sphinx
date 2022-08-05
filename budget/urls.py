from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_view, name='budget_view'),
    path('add_field/', views.add_field_to_db, name='add_field_to_db')
]