from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('registration/', views.registration_view, name='registration_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('change_password/', views.change_password_view, name='change_password_view')
]