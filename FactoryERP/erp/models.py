from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model for the Factory ERP system.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='viewer')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Vendor(models.Model):
    """
    Vendor/Supplier information for purchasing materials and services.
    """
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product catalog - finished goods or product types.
    """
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['sku']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"


class Material(models.Model):
    """
    Raw materials used in manufacturing.
    """
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)  # e.g., 'kg', 'liter', 'pieces'
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['sku']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"


class ProductMaterial(models.Model):
    """
    Bill of Materials (BOM) - Many-to-Many relationship between Products and Materials.
    Defines which materials are required for each product and in what quantities.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='products')
    required_qty = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Material'
        verbose_name_plural = 'Product Materials'
        unique_together = ['product', 'material']
        ordering = ['product', 'material']
    
    def __str__(self):
        return f"{self.product.sku} - {self.material.sku} (Qty: {self.required_qty})"


class Quotation(models.Model):
    """
    Vendor quotations for materials or services.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='quotations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quotations')
    quotation_no = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quotations_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.quotation_no} - {self.vendor.name}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


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
