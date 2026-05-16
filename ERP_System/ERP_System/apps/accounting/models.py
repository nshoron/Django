
from django.db import models


class LedgerAccount(models.Model):
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_name


class AccountingTransaction(models.Model):
    b2b_sale = models.ForeignKey(
        'sales_b2b.B2BSale',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    b2c_sale = models.ForeignKey(
        'sales_b2c.B2CSale',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    purchase = models.ForeignKey(
        'purchases.Purchase',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    expense = models.ForeignKey(
        'expenses.Expense',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    payment = models.ForeignKey(
        'payments.Payment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    ledger_account = models.ForeignKey(
        'accounting.LedgerAccount',
        on_delete=models.CASCADE
    )
    entry_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type}: {self.amount}"
