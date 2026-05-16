from django.db import models
from masters.models import Vendor, Material
from work_orders.models import WorkOrder
from accounts.models import User


class PurchaseOrder(models.Model):
    """
    Purchase orders sent to vendors for material procurement.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders')
    po_no = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    order_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase_orders_created')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders_approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-order_date']
    
    def __str__(self):
        return f"{self.po_no} - {self.vendor.name}"


class StockIn(models.Model):
    """
    Material receipt log - tracks incoming materials from purchase orders.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='stock_ins')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='stock_ins')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    received_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Stock In'
        verbose_name_plural = 'Stock In'
        ordering = ['-received_date']
    
    def __str__(self):
        return f"{self.purchase_order.po_no} - {self.material.sku} ({self.quantity})"
