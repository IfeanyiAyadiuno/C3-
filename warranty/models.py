from django.db import models

class Claim(models.Model):
    claim_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    warranty_type = models.CharField(max_length=100)
    warranty_category = models.CharField(max_length=100, blank=True, null=True)
    inspection_date = models.DateField()
    date_issued = models.DateField()
    status = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=100)
    initiated_by = models.CharField(max_length=100, blank=True, null=True)

    vin = models.CharField(max_length=50, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    odometer = models.PositiveIntegerField(blank=True, null=True)
    incident_description = models.TextField(blank=True, null=True)
    dealership_notes = models.TextField(blank=True, null=True)

    estimate_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    c3_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.claim_number} - {self.customer_name}"


class Policy(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    policy_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.policy_number} - {self.first_name} {self.last_name}"
