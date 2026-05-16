from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Product, Material, Quotation, WorkOrder, 
    PurchaseOrder, Inventory, ProductionLog, QCReport
)


# Dashboard Views
class DashboardView(LoginRequiredMixin, View):
    """Main dashboard view."""
    def get(self, request):
        context = {
            'total_products': Product.objects.count(),
            'total_materials': Material.objects.count(),
            'pending_quotations': Quotation.objects.filter(status='draft').count(),
            'active_work_orders': WorkOrder.objects.filter(status__in=['planned', 'in_progress']).count(),
            'pending_purchase_orders': PurchaseOrder.objects.filter(status='submitted').count(),
        }
        return render(request, 'erp/dashboard.html', context)


# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    """List all products."""
    model = Product
    template_name = 'erp/product_list.html'
    paginate_by = 20


class ProductDetailView(LoginRequiredMixin, DetailView):
    """View product details."""
    model = Product
    template_name = 'erp/product_detail.html'


# Material Views
class MaterialListView(LoginRequiredMixin, ListView):
    """List all materials."""
    model = Material
    template_name = 'erp/material_list.html'
    paginate_by = 20


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """View material details."""
    model = Material
    template_name = 'erp/material_detail.html'


# Quotation Views
class QuotationListView(LoginRequiredMixin, ListView):
    """List quotations."""
    model = Quotation
    template_name = 'erp/quotation_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Quotation.objects.select_related('vendor', 'product')


class QuotationDetailView(LoginRequiredMixin, DetailView):
    """View quotation details."""
    model = Quotation
    template_name = 'erp/quotation_detail.html'


# Work Order Views
class WorkOrderListView(LoginRequiredMixin, ListView):
    """List work orders."""
    model = WorkOrder
    template_name = 'erp/work_order_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return WorkOrder.objects.select_related('product', 'quotation')


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    """View work order details."""
    model = WorkOrder
    template_name = 'erp/work_order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work_order = self.get_object()
        context['materials'] = work_order.materials.all()
        context['production_logs'] = work_order.production_logs.all()
        context['qc_reports'] = work_order.qc_reports.all()
        return context


# Purchase Order Views
class PurchaseOrderListView(LoginRequiredMixin, ListView):
    """List purchase orders."""
    model = PurchaseOrder
    template_name = 'erp/purchase_order_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return PurchaseOrder.objects.select_related('vendor', 'work_order')


class PurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    """View purchase order details."""
    model = PurchaseOrder
    template_name = 'erp/purchase_order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = self.get_object()
        context['stock_ins'] = po.stock_ins.all()
        return context


# Inventory Views
class InventoryListView(LoginRequiredMixin, ListView):
    """List inventory."""
    model = Inventory
    template_name = 'erp/inventory_list.html'
    paginate_by = 20


# Production Log Views
class ProductionLogListView(LoginRequiredMixin, ListView):
    """List production logs."""
    model = ProductionLog
    template_name = 'erp/production_log_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductionLog.objects.select_related('work_order')


# QC Report Views
class QCReportListView(LoginRequiredMixin, ListView):
    """List QC reports."""
    model = QCReport
    template_name = 'erp/qc_report_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return QCReport.objects.select_related('work_order')


class QCReportDetailView(LoginRequiredMixin, DetailView):
    """View QC report details."""
    model = QCReport
    template_name = 'erp/qc_report_detail.html'
