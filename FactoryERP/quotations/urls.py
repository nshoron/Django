from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.QuotationListView.as_view(), name='list'),
    path('<int:pk>/', views.QuotationDetailView.as_view(), name='detail'),
]
