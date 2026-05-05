from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Return(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='returns'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='returns'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Return #{self.pk} - Order {self.order_id}'
    
class ReturnItem(models.Model):
    return_request = models.ForeignKey(
        Return,
        on_delete=models.CASCADE,
        related_name='items'
    )
    order_item = models.ForeignKey(
        'orders.OrderItem',
        on_delete=models.CASCADE,
        related_name='return_items'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['return_request', 'order_item'],
                name='unique_return_item'
            )
        ]

    def __str__(self):
        return f'ReturnItem {self.order_item_id} (x{self.quantity})'

class Refund(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]

    return_request = models.OneToOneField(
        Return,
        on_delete=models.CASCADE,
        related_name='refund'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True
    )
    refunded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Refund #{self.pk} - {self.amount}'