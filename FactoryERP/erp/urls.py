from django.urls import path
from . import views

app_name = 'erp'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Materials
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    
    # Quotations
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation_detail'),
    
    # Work Orders
    path('work-orders/', views.WorkOrderListView.as_view(), name='work_order_list'),
    path('work-orders/<int:pk>/', views.WorkOrderDetailView.as_view(), name='work_order_detail'),
    
    # Purchase Orders
    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-orders/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    
    # Inventory
    path('inventory/', views.InventoryListView.as_view(), name='inventory_list'),
    
    # Production Logs
    path('production-logs/', views.ProductionLogListView.as_view(), name='production_log_list'),
    
    # QC Reports
    path('qc-reports/', views.QCReportListView.as_view(), name='qc_report_list'),
    path('qc-reports/<int:pk>/', views.QCReportDetailView.as_view(), name='qc_report_detail'),
]
