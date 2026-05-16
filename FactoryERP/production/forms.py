from django import forms
from .models import ProductionLog, QCReport


class ProductionLogForm(forms.ModelForm):
    """Form for ProductionLog model."""
    
    class Meta:
        model = ProductionLog
        fields = ['work_order', 'start_time', 'end_time', 'produced_qty', 'status']


class QCReportForm(forms.ModelForm):
    """Form for QCReport model."""
    
    class Meta:
        model = QCReport
        fields = ['work_order', 'passed_qty', 'damaged_qty', 'remarks', 'status']
