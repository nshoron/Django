from django.db import models
from masters.models import Material, Product


class Inventory(models.Model):
    """
    Stock levels tracking for materials and products.
    """
    INVENTORY_TYPE_CHOICES = [
        ('material', 'Material'),
        ('product', 'Product'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='inventory')
    inventory_type = models.CharField(max_length=20, choices=INVENTORY_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'
        unique_together = [('material', 'product', 'inventory_type')]
        ordering = ['updated_at']
    
    def __str__(self):
        item = self.material or self.product
        return f"{item} - Stock: {self.quantity}"
    
    def is_low_stock(self):
        """Check if stock is below reorder level."""
        return self.quantity <= self.reorder_level
