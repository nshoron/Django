from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quotation


class QuotationListView(LoginRequiredMixin, ListView):
    """List quotations."""
    model = Quotation
    template_name = 'quotations/quotation_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Quotation.objects.select_related('vendor', 'product')


class QuotationDetailView(LoginRequiredMixin, DetailView):
    """View quotation details."""
    model = Quotation
    template_name = 'quotations/quotation_detail.html'
