from django.db import models
from quotations.models import Quotation
from masters.models import Product, Material
from accounts.models import User


class WorkOrder(models.Model):
    """
    Manufacturing work orders - tracks production orders for products.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='work_orders')
    work_order_no = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    machine_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    per_piece_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    deadline = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='work_orders_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.work_order_no} - {self.product.sku}"
    
    def save(self, *args, **kwargs):
        self.total_cost = self.material_cost + self.labor_cost + self.machine_cost + self.overhead_cost
        if self.quantity > 0:
            self.per_piece_cost = self.total_cost / self.quantity
        super().save(*args, **kwargs)


class WorkOrderMaterial(models.Model):
    """
    Materials required for a specific work order.
    Tracks material usage for each work order.
    """
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='work_order_usages')
    required_qty = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Work Order Material'
        verbose_name_plural = 'Work Order Materials'
        unique_together = ['work_order', 'material']
        ordering = ['work_order']
    
    def __str__(self):
        return f"{self.work_order.work_order_no} - {self.material.sku}"
    
    def save(self, *args, **kwargs):
        self.total_cost = self.required_qty * self.material.unit_cost
        super().save(*args, **kwargs)
