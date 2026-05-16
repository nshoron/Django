from django.test import TestCase
from .models import (
    User, Vendor, Product, Material, ProductMaterial,
    Quotation, WorkOrder, WorkOrderMaterial, Inventory,
    PurchaseOrder, StockIn, ProductionLog, QCReport,
    FinishedGoods, StockOut
)


class UserModelTest(TestCase):
    """Test User model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='admin'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'admin')


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


class QuotationModelTest(TestCase):
    """Test Quotation model."""
    
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact='John Doe',
            phone='1234567890',
            email='vendor@test.com',
            address='123 Test St'
        )
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            price=100.00
        )
        self.quotation = Quotation.objects.create(
            vendor=self.vendor,
            product=self.product,
            quotation_no='QT-001',
            quantity=10,
            unit_price=95.00
        )
    
    def test_quotation_total_price_calculation(self):
        self.assertEqual(self.quotation.total_price, 950.00)


class WorkOrderModelTest(TestCase):
    """Test WorkOrder model."""
    
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            price=100.00
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        from datetime import date
        self.work_order = WorkOrder.objects.create(
            product=self.product,
            work_order_no='WO-001',
            quantity=100,
            material_cost=500,
            labor_cost=300,
            machine_cost=200,
            overhead_cost=100,
            deadline=date.today(),
            created_by=self.user
        )
    
    def test_work_order_total_cost_calculation(self):
        self.assertEqual(self.work_order.total_cost, 1100)
        self.assertEqual(self.work_order.per_piece_cost, 11.00)
