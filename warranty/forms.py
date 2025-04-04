from django import forms
from .models import Claim
from django.utils.timezone import now

class DealerClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'claim_number',
            'customer_name',
            'vin',
            'vehicle',
            'odometer',
            'warranty_type',
            'inspection_date',
            'incident_description',
            'dealership_notes',
        ]
        widgets = {
            'claim_number': forms.TextInput(attrs={'placeholder': 'e.g. CLM12345'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'e.g. John Doe'}),
            'vin': forms.TextInput(attrs={'placeholder': 'e.g. 1HGCM82633A004352'}),
            'vehicle': forms.TextInput(attrs={'placeholder': 'e.g. Ram 1500'}),
            'odometer': forms.NumberInput(attrs={'placeholder': 'e.g. 75000'}),
            'warranty_type': forms.TextInput(attrs={'placeholder': 'e.g. Paint, Rust, Fabric'}),
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'incident_description': forms.Textarea(attrs={'placeholder': 'Describe the issue in detail…'}),
            'dealership_notes': forms.Textarea(attrs={'placeholder': 'Any dealership-specific notes…'}),
        }

    def save(self, commit=True):
        claim = super().save(commit=False)
        claim.status = 'Pending'
        claim.date_issued = now()
        claim.assigned_to = 'Unassigned'
        if commit:
            claim.save()
        return claim




