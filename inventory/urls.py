from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    #Home Page
    path('', views.index, name ='index'),
    path('view-inventory/', views.viewInventory, name = 'view-inventory'),
    path('add-inventory-item/', views.addInventory, name='add-inventory-item'),
    path('record-sale/', views.record_sale, name='record-sale'),
    path('increase-inventory/', views.increaseInventory, name = 'increase-inventory'),
]