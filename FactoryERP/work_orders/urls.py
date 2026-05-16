from django.urls import path
from . import views

app_name = 'work_orders'

urlpatterns = [
    path('', views.WorkOrderListView.as_view(), name='list'),
    path('<int:pk>/', views.WorkOrderDetailView.as_view(), name='detail'),
]
