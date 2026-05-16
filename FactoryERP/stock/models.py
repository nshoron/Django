from django.db import models
from masters.models import Product
from work_orders.models import WorkOrder


class StockOut(models.Model):
    """
    Stock out log - tracks outgoing products/materials.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_outs')
    quantity = models.IntegerField()
    out_date = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=255)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_outs')
    
    class Meta:
        verbose_name = 'Stock Out'
        verbose_name_plural = 'Stock Out'
        ordering = ['-out_date']
    
    def __str__(self):
        return f"{self.product.sku} - {self.quantity} units (To: {self.destination})"
