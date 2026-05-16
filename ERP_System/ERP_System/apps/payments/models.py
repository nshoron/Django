
from django.db import models


class Payment(models.Model):
    invoice = models.ForeignKey(
        'sales_b2b.Invoice',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    bill = models.ForeignKey(
        'sales_b2c.Bill',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    payment_type = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=50)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.payment_status}"


class PaymentTransaction(models.Model):
    payment = models.ForeignKey(
        'payments.Payment',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    transaction_number = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} - {self.amount}"
