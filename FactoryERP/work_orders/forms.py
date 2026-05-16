from django import forms
from .models import WorkOrder, WorkOrderMaterial


class WorkOrderForm(forms.ModelForm):
    """Form for WorkOrder model."""
    
    class Meta:
        model = WorkOrder
        fields = [
            'quotation', 'product', 'work_order_no', 'quantity',
            'material_cost', 'labor_cost', 'machine_cost', 'overhead_cost',
            'status', 'deadline'
        ]


class WorkOrderMaterialForm(forms.ModelForm):
    """Form for WorkOrderMaterial model."""
    
    class Meta:
        model = WorkOrderMaterial
        fields = ['work_order', 'material', 'required_qty']
