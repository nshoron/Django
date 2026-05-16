from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PurchaseOrder


class PurchaseOrderListView(LoginRequiredMixin, ListView):
    """List purchase orders."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return PurchaseOrder.objects.select_related('vendor', 'work_order')


class PurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    """View purchase order details."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = self.get_object()
        context['stock_ins'] = po.stock_ins.all()
        return context
