from django.contrib import admin
from .models import WorkOrder, WorkOrderMaterial


class WorkOrderMaterialInline(admin.TabularInline):
    model = WorkOrderMaterial
    extra = 1


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('work_order_no', 'product', 'quantity', 'status', 'deadline')
    search_fields = ('work_order_no', 'product__sku')
    list_filter = ('status', 'deadline', 'created_at')
    readonly_fields = ('total_cost', 'per_piece_cost', 'created_at', 'updated_at')
    inlines = [WorkOrderMaterialInline]


@admin.register(WorkOrderMaterial)
class WorkOrderMaterialAdmin(admin.ModelAdmin):
    list_display = ('work_order', 'material', 'required_qty', 'total_cost')
    search_fields = ('work_order__work_order_no', 'material__sku')
    list_filter = ('work_order',)
    readonly_fields = ('total_cost',)
