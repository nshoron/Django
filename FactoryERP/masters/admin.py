from django.contrib import admin
from .models import Vendor, Product, Material, ProductMaterial


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'phone')
    search_fields = ('name', 'email', 'contact')
    list_filter = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price')
    search_fields = ('sku', 'name')
    list_filter = ('created_at',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'unit', 'unit_cost')
    search_fields = ('sku', 'name')
    list_filter = ('unit', 'created_at')


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('product', 'material', 'required_qty')
    search_fields = ('product__sku', 'material__sku')
    list_filter = ('product',)
