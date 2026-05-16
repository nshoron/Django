from django import forms
from .models import Quotation


class QuotationForm(forms.ModelForm):
    """Form for Quotation model."""
    
    class Meta:
        model = Quotation
        fields = ['vendor', 'product', 'quotation_no', 'quantity', 'unit_price', 'status']
