from django.contrib import admin
from .models import LedgerAccount, AccountingTransaction


class AccountingTransactionInline(admin.TabularInline):
    model = AccountingTransaction
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["entry_type", "amount", "description", "created_at"]
    can_delete = False


@admin.register(LedgerAccount)
class LedgerAccountAdmin(admin.ModelAdmin):
    list_display = ["account_name", "account_type", "opening_balance", "current_balance"]
    list_filter = ["account_type", "created_at"]
    search_fields = ["account_name"]
    readonly_fields = ["created_at"]
    inlines = [AccountingTransactionInline]


@admin.register(AccountingTransaction)
class AccountingTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "ledger_account", "entry_type", "amount", "created_at"]
    list_filter = ["entry_type", "created_at", "ledger_account__account_type"]
    search_fields = ["description", "ledger_account__account_name"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
