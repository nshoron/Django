from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import *
from .serializers import *
from .services import *
from core.permissions import IsAdminManagerOrWarehouseStaff


class CustomerViewSet(ModelViewSet):
    queryset = B2BCustomer.objects.all()
    serializer_class = B2BCustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['company_name', 'contact_name', 'email', 'phone']
    ordering_fields = ['company_name']


class SaleViewSet(ModelViewSet):
    queryset = B2BSale.objects.select_related("b2b_customer", "created_by").prefetch_related("items")
    serializer_class = B2BSaleSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['b2b_customer__company_name', 'id']
    ordering_fields = ['created_at', 'total_amount']

    def perform_create(self, serializer):
        sale = serializer.save(created_by=self.request.user)
        generate_invoice(sale)

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get("customer")

        if customer_id:
            queryset = queryset.filter(b2b_customer_id=customer_id)

        return queryset
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get sales by customer"""
        customer_id = request.query_params.get('customer_id')
        if customer_id:
            sales = B2BSale.objects.filter(b2b_customer_id=customer_id)
            serializer = self.get_serializer(sales, many=True)
            return Response(serializer.data)
        return Response({'error': 'customer_id is required'}, status=400)


class SaleItemViewSet(ModelViewSet):
    queryset = B2BSaleItem.objects.select_related("b2b_sale", "product_variant")
    serializer_class = B2BSaleItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['product_variant__product_code']

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_b2b_sale_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.select_related("b2b_sale")
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['invoice_number']
    ordering_fields = ['created_at', 'due_date']


class ReturnViewSet(ModelViewSet):
    queryset = B2BReturn.objects.select_related("b2b_sale", "created_by").prefetch_related("items")
    serializer_class = B2BReturnSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['b2b_sale__id']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReturnItemViewSet(ModelViewSet):
    queryset = B2BReturnItem.objects.select_related(
        "b2b_return",
        "b2b_sale_item",
        "b2b_sale_item__product_variant",
    )
    serializer_class = B2BReturnItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_b2b_return_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))
