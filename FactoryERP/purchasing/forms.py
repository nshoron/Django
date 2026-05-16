from django import forms
from .models import PurchaseOrder, StockIn


class PurchaseOrderForm(forms.ModelForm):
    """Form for PurchaseOrder model."""
    
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'work_order', 'po_no', 'total_amount', 'status', 'order_date']


class StockInForm(forms.ModelForm):
    """Form for StockIn model."""
    
    class Meta:
        model = StockIn
        fields = ['purchase_order', 'material', 'quantity']
