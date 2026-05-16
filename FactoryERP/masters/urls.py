from django.urls import path
from . import views

app_name = 'masters'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor_detail'),
]
