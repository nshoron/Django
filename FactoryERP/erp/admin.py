from django.contrib import admin
from .models import (
    User, Vendor, Product, Material, ProductMaterial,
    Quotation, WorkOrder, WorkOrderMaterial, Inventory,
    PurchaseOrder, StockIn, ProductionLog, QCReport,
    FinishedGoods, StockOut
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'created')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created')}),
    )


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


class ProductMaterialInline(admin.TabularInline):
    model = ProductMaterial
    extra = 1


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('product', 'material', 'required_qty')
    search_fields = ('product__sku', 'material__sku')
    list_filter = ('product',)


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_no', 'vendor', 'product', 'quantity', 'total_price', 'status')
    search_fields = ('quotation_no', 'vendor__name', 'product__sku')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_price', 'created_at', 'updated_at')


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


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'inventory_type', 'quantity', 'reorder_level', 'is_low_stock')
    search_fields = ('material__sku', 'product__sku')
    list_filter = ('inventory_type', 'updated_at')
    readonly_fields = ('updated_at',)


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


@admin.register(FinishedGoods)
class FinishedGoodsAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'work_order', 'created_at')
    search_fields = ('product__sku', 'work_order__work_order_no')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'destination', 'out_date')
    search_fields = ('product__sku', 'destination')
    list_filter = ('out_date',)
    readonly_fields = ('out_date',)
