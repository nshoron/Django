from django.contrib import admin
from .models import Quotation


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_no', 'vendor', 'product', 'quantity', 'total_price', 'status')
    search_fields = ('quotation_no', 'vendor__name', 'product__sku')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
