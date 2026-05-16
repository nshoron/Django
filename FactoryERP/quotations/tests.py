from django.test import TestCase
from accounts.models import User
from masters.models import Vendor, Product
from .models import Quotation


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
