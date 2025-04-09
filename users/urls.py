from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),  # Use your custom login view
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dealer-login/', views.dealer_login, name='dealer_login'),
    path('dealer/', views.dealer_dashboard, name='dealer_dashboard'),
    path('dealer/record-sale/', views.record_sale, name='record_sale'),
    path('dealer/submit-claim/', views.submit_claim, name='submit_claim'),
    path('dealer/update-claim/', views.update_claim, name='update_claim'),
]
