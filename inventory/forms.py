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
                  'sell':'Sale Price',
                  'quantity':'Quantity'}
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = {'item',
                  'quantity'
        }
        labels = {'item':'Item Name',
                  'quantity':'Quantity'}
        
class AddStockForm(forms.ModelForm):
    class Meta:
        model = Sale  # If using a different model, update this line
        fields = ['item', 'quantity']  # Ensure 'item' is a ForeignKey to Item

        labels = {
            'item': 'Select Item',
            'quantity': 'Quantity to Add',
        }