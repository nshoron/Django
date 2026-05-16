from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Material, Vendor


class ProductListView(LoginRequiredMixin, ListView):
    """List all products."""
    model = Product
    template_name = 'masters/product_list.html'
    paginate_by = 20


class ProductDetailView(LoginRequiredMixin, DetailView):
    """View product details."""
    model = Product
    template_name = 'masters/product_detail.html'


class MaterialListView(LoginRequiredMixin, ListView):
    """List all materials."""
    model = Material
    template_name = 'masters/material_list.html'
    paginate_by = 20


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """View material details."""
    model = Material
    template_name = 'masters/material_detail.html'


class VendorListView(LoginRequiredMixin, ListView):
    """List all vendors."""
    model = Vendor
    template_name = 'masters/vendor_list.html'
    paginate_by = 20


class VendorDetailView(LoginRequiredMixin, DetailView):
    """View vendor details."""
    model = Vendor
    template_name = 'masters/vendor_detail.html'
