#inventory/forms.py
from django import forms
from .models import Item, Sale

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = {'name',
                  'price',
                  'sell',
                  'quantity'}
        labels = {'name' :'Item Name',
                  'price':'Purchase Price',
                  'sell':'Sales Price',
                  'quantity':'Quantity'}
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = {'item',
                  'quantity'
        }
        labels = {'item':'Item Name',
                  'quantity':'Quantity'}