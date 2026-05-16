from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Inventory


class InventoryListView(LoginRequiredMixin, ListView):
    """List inventory."""
    model = Inventory
    template_name = 'inventory/inventory_list.html'
    paginate_by = 20
