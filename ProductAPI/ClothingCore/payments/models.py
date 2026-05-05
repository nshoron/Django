from django.db import models


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Card'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payment'
    )
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'Payment #{self.pk} - Order {self.order_id} ({self.status})'