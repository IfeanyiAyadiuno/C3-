from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),  # Use your custom login view
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
