from django.contrib import admin
from .models import StockOut


@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'destination', 'out_date')
    search_fields = ('product__sku', 'destination')
    list_filter = ('out_date',)
    readonly_fields = ('out_date',)
