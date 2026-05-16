from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WorkOrder


class WorkOrderListView(LoginRequiredMixin, ListView):
    """List work orders."""
    model = WorkOrder
    template_name = 'work_orders/work_order_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return WorkOrder.objects.select_related('product', 'quotation')


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    """View work order details."""
    model = WorkOrder
    template_name = 'work_orders/work_order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work_order = self.get_object()
        context['materials'] = work_order.materials.all()
        return context
