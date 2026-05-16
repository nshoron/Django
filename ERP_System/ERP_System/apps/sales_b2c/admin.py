from django.contrib import admin
from .models import B2CCustomer, B2CSale, B2CSaleItem, Bill, B2CReturn, B2CReturnItem


class B2CSaleItemInline(admin.TabularInline):
    model = B2CSaleItem
    extra = 1
    fields = ["product_variant", "quantity", "unit_price"]


class B2CReturnItemInline(admin.TabularInline):
    model = B2CReturnItem
    extra = 0
    fields = ["sale_item", "quantity", "refund_amount"]


@admin.register(B2CCustomer)
class B2CCustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email"]
    search_fields = ["name", "phone", "email"]
    ordering = ["name"]


@admin.register(B2CSale)
class B2CSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "total_amount", "payment_method", "created_at"]
    list_filter = ["payment_method", "created_at", "customer"]
    search_fields = ["customer__name"]
    readonly_fields = ["created_at"]
    inlines = [B2CSaleItemInline]
    date_hierarchy = "created_at"


@admin.register(B2CSaleItem)
class B2CSaleItemAdmin(admin.ModelAdmin):
    list_display = ["id", "sale", "product_variant", "quantity", "unit_price"]
    list_filter = ["sale"]
    search_fields = ["product_variant__product_code"]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ["bill_number", "sale", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["bill_number"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"


@admin.register(B2CReturn)
class B2CReturnAdmin(admin.ModelAdmin):
    list_display = ["id", "sale", "total_refund", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["sale__id"]
    readonly_fields = ["created_at"]
    inlines = [B2CReturnItemInline]
    date_hierarchy = "created_at"


@admin.register(B2CReturnItem)
class B2CReturnItemAdmin(admin.ModelAdmin):
    list_display = ["id", "b2c_return", "sale_item", "quantity", "refund_amount"]
    list_filter = ["b2c_return"]
    search_fields = ["b2c_return__id"]
