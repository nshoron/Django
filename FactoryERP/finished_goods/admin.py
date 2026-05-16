from django.contrib import admin
from .models import FinishedGoods


@admin.register(FinishedGoods)
class FinishedGoodsAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'work_order', 'created_at')
    search_fields = ('product__sku', 'work_order__work_order_no')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
