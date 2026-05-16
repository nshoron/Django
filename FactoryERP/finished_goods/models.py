from django.db import models
from work_orders.models import WorkOrder
from masters.models import Product


class FinishedGoods(models.Model):
    """
    Finished goods inventory - tracks completed products from work orders.
    """
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='finished_goods')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='finished_goods')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Finished Goods'
        verbose_name_plural = 'Finished Goods'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.sku} - {self.quantity} units"
