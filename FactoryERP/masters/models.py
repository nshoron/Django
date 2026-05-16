from django.db import models


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
