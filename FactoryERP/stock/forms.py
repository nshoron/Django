from django import forms
from .models import StockOut


class StockOutForm(forms.ModelForm):
    """Form for StockOut model."""
    
    class Meta:
        model = StockOut
        fields = ['product', 'quantity', 'destination', 'work_order']
