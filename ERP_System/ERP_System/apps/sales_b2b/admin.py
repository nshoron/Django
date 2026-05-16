from django.contrib import admin
from .models import B2BCustomer, B2BSale, B2BSaleItem, Invoice, B2BReturn, B2BReturnItem


class B2BSaleItemInline(admin.TabularInline):
    model = B2BSaleItem
    extra = 1
    fields = ["product_variant", "quantity", "unit_price"]


class B2BReturnItemInline(admin.TabularInline):
    model = B2BReturnItem
    extra = 0
    fields = ["b2b_sale_item", "quantity"]


@admin.register(B2BCustomer)
class B2BCustomerAdmin(admin.ModelAdmin):
    list_display = ["company_name", "contact_name", "phone", "email"]
    search_fields = ["company_name", "contact_name", "email", "phone"]
    list_filter = ["company_name"]
    ordering = ["company_name"]


@admin.register(B2BSale)
class B2BSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "b2b_customer", "total_amount", "created_at"]
    list_filter = ["created_at", "b2b_customer"]
    search_fields = ["b2b_customer__company_name"]
    readonly_fields = ["created_at"]
    inlines = [B2BSaleItemInline]
    date_hierarchy = "created_at"


@admin.register(B2BSaleItem)
class B2BSaleItemAdmin(admin.ModelAdmin):
    list_display = ["id", "b2b_sale", "product_variant", "quantity", "unit_price"]
    list_filter = ["b2b_sale"]
    search_fields = ["product_variant__product_code"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "b2b_sale", "status", "due_date", "created_at"]
    list_filter = ["status", "created_at", "due_date"]
    search_fields = ["invoice_number"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"


@admin.register(B2BReturn)
class B2BReturnAdmin(admin.ModelAdmin):
    list_display = ["id", "b2b_sale", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["b2b_sale__id"]
    readonly_fields = ["created_at"]
    inlines = [B2BReturnItemInline]
    date_hierarchy = "created_at"


@admin.register(B2BReturnItem)
class B2BReturnItemAdmin(admin.ModelAdmin):
    list_display = ["id", "b2b_return", "b2b_sale_item", "quantity"]
    list_filter = ["b2b_return"]
    search_fields = ["b2b_return__id"]
