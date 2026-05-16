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
    queryset = B2CCustomer.objects.all()
    serializer_class = B2CCustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name']


class SaleViewSet(ModelViewSet):
    queryset = B2CSale.objects.select_related("customer", "created_by").prefetch_related("items")
    serializer_class = B2CSaleSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['customer__name', 'id']
    ordering_fields = ['created_at', 'total_amount']

    def perform_create(self, serializer):
        customer = serializer.validated_data.get("customer")
        if customer is None:
            customer, _ = B2CCustomer.objects.get_or_create(
                name="Walk-in Customer",
                defaults={"phone": "", "email": ""},
            )

        sale = serializer.save(created_by=self.request.user, customer=customer)
        generate_bill(sale)

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get("customer")
        payment_method = self.request.query_params.get("payment_method")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get sales by customer"""
        customer_id = request.query_params.get('customer_id')
        if customer_id:
            sales = B2CSale.objects.filter(customer_id=customer_id)
            serializer = self.get_serializer(sales, many=True)
            return Response(serializer.data)
        return Response({'error': 'customer_id is required'}, status=400)


class SaleItemViewSet(ModelViewSet):
    queryset = B2CSaleItem.objects.select_related("sale", "product_variant")
    serializer_class = B2CSaleItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['product_variant__product_code']

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_sale_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))


class BillViewSet(ModelViewSet):
    queryset = Bill.objects.select_related("sale")
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['bill_number']
    ordering_fields = ['created_at']


class ReturnViewSet(ModelViewSet):
    queryset = B2CReturn.objects.select_related("sale", "created_by").prefetch_related("items")
    serializer_class = B2CReturnSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['sale__id']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReturnItemViewSet(ModelViewSet):
    queryset = B2CReturnItem.objects.select_related(
        "b2c_return",
        "sale_item",
        "sale_item__product_variant",
    )
    serializer_class = B2CReturnItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_return_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))
