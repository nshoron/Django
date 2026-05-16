from django.contrib import admin
from .models import Payment, PaymentTransaction


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["amount", "transaction_type", "payment_method", "transaction_number", "created_at"]
    can_delete = False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "payment_type", "total_amount", "paid_amount", "due_amount", "payment_status", "created_at"]
    list_filter = ["payment_status", "payment_type", "created_at"]
    search_fields = ["id"]
    readonly_fields = ["created_at", "paid_amount", "due_amount"]
    inlines = [PaymentTransactionInline]
    date_hierarchy = "created_at"


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "payment", "amount", "transaction_type", "payment_method", "created_at"]
    list_filter = ["transaction_type", "payment_method", "created_at"]
    search_fields = ["payment__id", "transaction_number"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
