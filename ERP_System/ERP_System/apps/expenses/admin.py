from django.contrib import admin
from .models import ExpenseCategory, Expense


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["title", "expense_category", "amount", "payment_method", "created_at"]
    list_filter = ["expense_category", "payment_method", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
