from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inspection_index'),
    path('tickets/', views.inspection_tickets, name='inspection_tickets'),
    path('assign-inspector/', views.assign_inspector, name='assign_inspector'),
    path('schedule-inspection/<int:ticket_id>/', views.schedule_inspection, name='schedule_inspection'),
    path('schedule-inspection/', views.schedule_inspection, name='schedule_inspection_no_ticket'),
    path('create-ticket/', views.create_inspection_ticket, name='create_inspection_ticket'),
    path('create-inspector/', views.create_inspector, name='create_inspector'),
    path('complete-inspection/<int:ticket_id>/', views.complete_inspection, name='complete_inspection'),
    path('complete-inspection/', views.complete_inspection, name='complete_inspection_no_ticket'),
    path('view-inspection/<int:ticket_id>/', views.view_inspection, name='view_inspection'),
    path('view-inspection/', views.view_inspection, name='view_inspection_no_ticket'),
    path('delete-ticket/<int:ticket_id>/', views.delete_inspection_ticket, name='delete_inspection_ticket'),
]
