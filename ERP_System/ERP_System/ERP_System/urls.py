"""
URL configuration for ERP_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core.reports import (
    dashboard_summary,
    inventory_report,
    low_stock_report,
    sales_report,
    purchase_report,
    supplier_report,
    customer_report,
    payment_report,
    expense_report,
    profit_loss_report,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/inventory/", include("apps.inventory.urls")),
    path("api/purchases/", include("apps.purchases.urls")),
    path("api/b2b/", include("apps.sales_b2b.urls")),
    path("api/b2c/", include("apps.sales_b2c.urls")),
    path("api/accounting/", include("apps.accounting.urls")),
    path("api/expenses/", include("apps.expenses.urls")),
    path("api/", include("apps.payments.urls")),
    
    # Reports & Dashboard
    path("api/reports/dashboard/", dashboard_summary, name="dashboard"),
    path("api/reports/inventory/", inventory_report, name="inventory_report"),
    path("api/reports/low-stock/", low_stock_report, name="low_stock_report"),
    path("api/reports/sales/", sales_report, name="sales_report"),
    path("api/reports/purchases/", purchase_report, name="purchase_report"),
    path("api/reports/suppliers/", supplier_report, name="supplier_report"),
    path("api/reports/customers/", customer_report, name="customer_report"),
    path("api/reports/payments/", payment_report, name="payment_report"),
    path("api/reports/expenses/", expense_report, name="expense_report"),
    path("api/reports/profit-loss/", profit_loss_report, name="profit_loss_report"),
]
