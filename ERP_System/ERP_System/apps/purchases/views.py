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


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name']


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.select_related("supplier", "created_by").prefetch_related("items")
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['supplier__name', 'id']
    ordering_fields = ['created_at', 'total_amount']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier_id = self.request.query_params.get("supplier")
        status_value = self.request.query_params.get("status")

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset
    
    @action(detail=False, methods=['get'])
    def by_supplier(self, request):
        """Get purchases by supplier"""
        supplier_id = request.query_params.get('supplier_id')
        if supplier_id:
            purchases = Purchase.objects.filter(supplier_id=supplier_id)
            serializer = self.get_serializer(purchases, many=True)
            return Response(serializer.data)
        return Response({'error': 'supplier_id is required'}, status=400)

    @action(detail=False, methods=['get'], url_path="supplier-report")
    def supplier_report(self, request):
        supplier_id = request.query_params.get("supplier_id")
        queryset = self.get_queryset()
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        data = []
        for supplier in Supplier.objects.all():
            purchases = queryset.filter(supplier=supplier)
            if supplier_id and str(supplier.id) != str(supplier_id):
                continue
            data.append({
                "supplier_id": supplier.id,
                "supplier": supplier.name,
                "purchase_count": purchases.count(),
                "total_amount": sum((purchase.total_amount for purchase in purchases), 0),
            })

        return Response(data)


class PurchaseItemViewSet(ModelViewSet):
    queryset = PurchaseItem.objects.select_related("purchase", "product_variant")
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['product_variant__product_code']

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_purchase_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))


class PurchaseReturnViewSet(ModelViewSet):
    queryset = PurchaseReturn.objects.select_related("purchase", "supplier", "created_by").prefetch_related("items")
    serializer_class = PurchaseReturnSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = ['supplier__name', 'id']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        purchase = serializer.validated_data["purchase"]
        serializer.save(created_by=self.request.user, supplier=purchase.supplier)


class PurchaseReturnItemViewSet(ModelViewSet):
    queryset = PurchaseReturnItem.objects.select_related(
        "purchase_return",
        "purchase_item",
        "purchase_item__product_variant",
    )
    serializer_class = PurchaseReturnItemSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                item = serializer.save()
                process_purchase_return_item(
                    item,
                    self.request.user
                )
        except ValueError as exc:
            raise ValidationError(str(exc))
