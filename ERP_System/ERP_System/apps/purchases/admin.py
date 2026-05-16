from django.contrib import admin
from .models import Supplier, Purchase, PurchaseItem, PurchaseReturn, PurchaseReturnItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    fields = ["product_variant", "quantity", "unit_cost"]


class PurchaseReturnItemInline(admin.TabularInline):
    model = PurchaseReturnItem
    extra = 0
    fields = ["purchase_item", "quantity"]
    readonly_fields = ["purchase_item"]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email"]
    search_fields = ["name", "email", "phone"]
    ordering = ["name"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "supplier", "total_amount", "status", "created_at"]
    list_filter = ["status", "created_at", "supplier"]
    search_fields = ["supplier__name"]
    readonly_fields = ["created_at"]
    inlines = [PurchaseItemInline]
    date_hierarchy = "created_at"


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ["id", "purchase", "product_variant", "quantity", "unit_cost"]
    list_filter = ["purchase"]
    search_fields = ["product_variant__product_code"]


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = ["id", "purchase", "supplier", "created_at"]
    list_filter = ["created_at", "supplier"]
    search_fields = ["purchase__id"]
    readonly_fields = ["created_at"]
    inlines = [PurchaseReturnItemInline]
    date_hierarchy = "created_at"


@admin.register(PurchaseReturnItem)
class PurchaseReturnItemAdmin(admin.ModelAdmin):
    list_display = ["id", "purchase_return", "purchase_item", "quantity"]
    list_filter = ["purchase_return"]
    search_fields = ["purchase_return__id"]
