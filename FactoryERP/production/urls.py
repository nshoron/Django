from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('production-logs/', views.ProductionLogListView.as_view(), name='log_list'),
    path('qc-reports/', views.QCReportListView.as_view(), name='qc_list'),
    path('qc-reports/<int:pk>/', views.QCReportDetailView.as_view(), name='qc_detail'),
]
