from django.contrib import admin
from .models import ProductionLog, QCReport


@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('work_order', 'produced_qty', 'status', 'start_time')
    search_fields = ('work_order__work_order_no',)
    list_filter = ('status', 'start_time')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QCReport)
class QCReportAdmin(admin.ModelAdmin):
    list_display = ('work_order', 'passed_qty', 'damaged_qty', 'status')
    search_fields = ('work_order__work_order_no',)
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
