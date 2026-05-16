from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'inventory_type', 'quantity', 'reorder_level', 'is_low_stock')
    search_fields = ('material__sku', 'product__sku')
    list_filter = ('inventory_type', 'updated_at')
    readonly_fields = ('updated_at',)
