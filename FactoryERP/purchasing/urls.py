from django.urls import path
from . import views

app_name = 'purchasing'

urlpatterns = [
    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='po_list'),
    path('purchase-orders/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='po_detail'),
]
