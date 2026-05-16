from django import forms
from .models import (
    User, Vendor, Product, Material, ProductMaterial,
    Quotation, WorkOrder, WorkOrderMaterial, Inventory,
    PurchaseOrder, StockIn, ProductionLog, QCReport,
    FinishedGoods, StockOut
)


class UserForm(forms.ModelForm):
    """Form for User model."""
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']


class VendorForm(forms.ModelForm):
    """Form for Vendor model."""
    
    class Meta:
        model = Vendor
        fields = ['name', 'contact', 'phone', 'email', 'address']


class ProductForm(forms.ModelForm):
    """Form for Product model."""
    
    class Meta:
        model = Product
        fields = ['name', 'sku', 'price', 'description']


class MaterialForm(forms.ModelForm):
    """Form for Material model."""
    
    class Meta:
        model = Material
        fields = ['name', 'sku', 'unit', 'unit_cost', 'description']


class ProductMaterialForm(forms.ModelForm):
    """Form for ProductMaterial model."""
    
    class Meta:
        model = ProductMaterial
        fields = ['product', 'material', 'required_qty']


class QuotationForm(forms.ModelForm):
    """Form for Quotation model."""
    
    class Meta:
        model = Quotation
        fields = ['vendor', 'product', 'quotation_no', 'quantity', 'unit_price', 'status']


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


class InventoryForm(forms.ModelForm):
    """Form for Inventory model."""
    
    class Meta:
        model = Inventory
        fields = ['material', 'product', 'inventory_type', 'quantity', 'reorder_level']


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


class FinishedGoodsForm(forms.ModelForm):
    """Form for FinishedGoods model."""
    
    class Meta:
        model = FinishedGoods
        fields = ['work_order', 'product', 'quantity']


class StockOutForm(forms.ModelForm):
    """Form for StockOut model."""
    
    class Meta:
        model = StockOut
        fields = ['product', 'quantity', 'destination', 'work_order']
