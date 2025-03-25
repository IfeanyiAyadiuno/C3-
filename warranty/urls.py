from django.urls import path
from . import views

app_name = 'warranty'

urlpatterns = [
    path('', views.claims_landing, name='claims_landing'),
    path('claims/', views.claims_list, name='claims_list'),
    path('claims/<int:claim_id>/', views.claim_detail, name='claim_detail'),
    path('policies/search/', views.policies_search, name='policies_search'),
]

