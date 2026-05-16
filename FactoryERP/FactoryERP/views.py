from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from masters.models import Product, Material, Vendor
from quotations.models import Quotation
from work_orders.models import WorkOrder
from purchasing.models import PurchaseOrder
from inventory.models import Inventory


class DashboardView(LoginRequiredMixin, View):
    """Main dashboard view with ERP statistics."""
    
    def get(self, request):
        context = {
            'total_products': Product.objects.count(),
            'total_materials': Material.objects.count(),
            'total_vendors': Vendor.objects.count(),
            'pending_quotations': Quotation.objects.filter(status='draft').count(),
            'active_work_orders': WorkOrder.objects.filter(status__in=['planned', 'in_progress']).count(),
            'pending_purchase_orders': PurchaseOrder.objects.filter(status='submitted').count(),
            'low_stock_items': Inventory.objects.filter(quantity__lte=0).count(),
        }
        return render(request, 'dashboard.html', context)
