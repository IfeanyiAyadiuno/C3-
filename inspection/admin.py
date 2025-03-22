from django.contrib import admin
from .models import Inspector, InspectionTicket, InspectionSchedule

# Register your models here.
admin.site.register(Inspector)
admin.site.register(InspectionTicket)
admin.site.register(InspectionSchedule)
