from django import forms
from .models import FinishedGoods


class FinishedGoodsForm(forms.ModelForm):
    """Form for FinishedGoods model."""
    
    class Meta:
        model = FinishedGoods
        fields = ['work_order', 'product', 'quantity']
