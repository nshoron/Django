from django.db import models


class InventoryLog(models.Model):
    class ChangeType(models.TextChoices):
        ADD = 'add', 'Add'
        REMOVE = 'remove', 'Remove'
        RETURN = 'return', 'Return'

    product_variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        related_name='inventory_logs',
    )
    change_type = models.CharField(max_length=16, choices=ChangeType.choices)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.change_type} {self.quantity} (variant {self.product_variant_id})'
