from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProductionLog, QCReport


class ProductionLogListView(LoginRequiredMixin, ListView):
    """List production logs."""
    model = ProductionLog
    template_name = 'production/production_log_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductionLog.objects.select_related('work_order')


class QCReportListView(LoginRequiredMixin, ListView):
    """List QC reports."""
    model = QCReport
    template_name = 'production/qc_report_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return QCReport.objects.select_related('work_order')


class QCReportDetailView(LoginRequiredMixin, DetailView):
    """View QC report details."""
    model = QCReport
    template_name = 'production/qc_report_detail.html'
