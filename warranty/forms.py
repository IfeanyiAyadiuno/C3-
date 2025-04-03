from django import forms
from .models import Claim, Policy

class DealerClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'claim_number',
            'customer_name',
            'warranty_type',
            'inspection_date',
            'date_issued',
            'status',
            'assigned_to',
            'vin',
            'vehicle',
            'odometer',
            'incident_description',
            'dealership_notes',
            'estimate_amount',
            'c3_notes',
        ]
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'date_issued': forms.DateInput(attrs={'type': 'date'}),
        }

