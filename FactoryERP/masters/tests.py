from django.test import TestCase
from .models import Vendor, Product, Material


class ProductModelTest(TestCase):
    """Test Product model."""
    
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            price=100.00
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.sku, 'TEST-001')
        self.assertEqual(self.product.price, 100.00)


class MaterialModelTest(TestCase):
    """Test Material model."""
    
    def setUp(self):
        self.material = Material.objects.create(
            name='Test Material',
            sku='MAT-001',
            unit='kg',
            unit_cost=50.00
        )
    
    def test_material_creation(self):
        self.assertEqual(self.material.sku, 'MAT-001')
        self.assertEqual(self.material.unit_cost, 50.00)
