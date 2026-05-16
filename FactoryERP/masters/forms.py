from django import forms
from .models import Vendor, Product, Material, ProductMaterial


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
