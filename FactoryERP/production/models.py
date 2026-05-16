from django.db import models
from work_orders.models import WorkOrder
from accounts.models import User


class ProductionLog(models.Model):
    """
    Production logs - tracks production activities for each work order.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('aborted', 'Aborted'),
    ]
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='production_logs')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    produced_qty = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='production_logs_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Production Log'
        verbose_name_plural = 'Production Logs'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.work_order.work_order_no} - {self.produced_qty} units"


class QCReport(models.Model):
    """
    Quality Control reports - tracks quality inspection results.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ]
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='qc_reports')
    passed_qty = models.IntegerField()
    damaged_qty = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='qc_reports_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'QC Report'
        verbose_name_plural = 'QC Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"QC - {self.work_order.work_order_no} (Passed: {self.passed_qty})"
