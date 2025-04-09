from django.db import models
from django.utils import timezone

# Create your models here.
class Inspector(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Available')
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class InspectionTicket(models.Model):
    PRIORITY_CHOICES = (
        ('Critical', 'Critical'),
        ('Normal', 'Normal'),
    )
    
    TAG_CHOICES = (
        ('Tag 1', 'Tag 1'),
        ('No Tag Assigned', 'No Tag Assigned'),
    )
    
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
    )
    
    ticket_number = models.CharField(max_length=10, unique=True)
    inspection_type = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    vehicle_make = models.CharField(max_length=100)
    vin = models.CharField(max_length=100)
    inspector = models.ForeignKey(Inspector, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='No Tag Assigned')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    inspection_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.inspection_type}"

class InspectionSchedule(models.Model):
    ticket = models.OneToOneField(InspectionTicket, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    inspection_time = models.TimeField()
    duration = models.IntegerField(default=1)  # in hours
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Schedule for Ticket #{self.ticket.ticket_number} on {self.inspection_date}"
