from django.contrib import admin
from .models import Inventory, InventoryLog


class InventoryLogInline(admin.TabularInline):
    model = InventoryLog
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["type", "quantity", "previous_stock", "new_stock", "created_at"]
    can_delete = False


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "product_variant",
        "stock_quantity",
        "reorder_level",
        "cost_price",
        "retail_price",
        "status"
    ]
    list_filter = ["created_at"]
    search_fields = ["product_variant__product_code"]
    readonly_fields = ["created_at"]
    inlines = [InventoryLogInline]
    
    def status(self, obj):
        if obj.stock_quantity <= obj.reorder_level:
            return "Low Stock"
        return "In Stock"
    status.short_description = "Status"


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ["inventory", "type", "quantity", "previous_stock", "new_stock", "created_at"]
    list_filter = ["type", "created_at"]
    search_fields = ["inventory__product_variant__product_code"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
