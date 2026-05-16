from django.contrib import admin
from .models import PurchaseOrder, StockIn


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_no', 'vendor', 'total_amount', 'status', 'order_date')
    search_fields = ('po_no', 'vendor__name')
    list_filter = ('status', 'order_date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'material', 'quantity', 'received_date')
    search_fields = ('purchase_order__po_no', 'material__sku')
    list_filter = ('received_date',)
    readonly_fields = ('received_date',)
