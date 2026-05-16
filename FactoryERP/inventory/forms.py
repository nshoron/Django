from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    """Form for Inventory model."""
    
    class Meta:
        model = Inventory
        fields = ['material', 'product', 'inventory_type', 'quantity', 'reorder_level']
