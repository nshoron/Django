from django.test import TestCase
from datetime import date, timedelta
from accounts.models import User
from masters.models import Product
from .models import WorkOrder


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
