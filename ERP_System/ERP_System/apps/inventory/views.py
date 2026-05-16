from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F

from .models import Inventory, InventoryLog
from .serializers import (
    InventorySerializer,
    InventoryCreateSerializer,
    InventoryLogSerializer
)
from .services import ALL_ACTIONS, update_inventory
from core.permissions import IsAdminManagerOrWarehouseStaff


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.select_related(
        "product_variant",
        "product_variant__product",
        "product_variant__size",
        "product_variant__color",
    )
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = [
        "product_variant__product_code",
        "product_variant__product__name",
        "product_variant__size__name",
        "product_variant__color__name",
    ]
    ordering_fields = ["stock_quantity", "reorder_level", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        product_code = self.request.query_params.get("product_code")
        variant_id = self.request.query_params.get("product_variant")
        low_stock = self.request.query_params.get("low_stock")

        if product_code:
            queryset = queryset.filter(product_variant__product_code=product_code)
        if variant_id:
            queryset = queryset.filter(product_variant_id=variant_id)
        if low_stock in ["1", "true", "True"]:
            queryset = queryset.filter(stock_quantity__lte=F("reorder_level"))

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return InventorySerializer
        return InventoryCreateSerializer

    @action(detail=True, methods=["post"])
    def operate(self, request, pk=None):
        inventory = self.get_object()

        operation_type = request.data.get("type")
        quantity = request.data.get("quantity")
        reference_id = request.data.get("reference_id")
        reference_type = request.data.get("reference_type")

        if not operation_type:
            return Response(
                {"error": "type is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if operation_type not in ALL_ACTIONS:
            return Response(
                {"error": f"type must be one of: {', '.join(sorted(ALL_ACTIONS))}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity is None:
            return Response(
                {"error": "quantity is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "quantity must be a whole number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 0:
            return Response(
                {"error": "quantity cannot be negative"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            inventory = update_inventory(
                inventory=inventory,
                quantity=quantity,
                action=operation_type,
                user=request.user,
                reference_id=reference_id,
                reference_type=reference_type
            )

            return Response(
                {
                    "message": f"{operation_type} success",
                    "stock_quantity": inventory.stock_quantity,
                },
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"], url_path="reorder-alerts")
    def reorder_alerts(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(stock_quantity__lte=F("reorder_level"))
        )
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        inventory = self.get_object()
        logs = inventory.logs.select_related("created_by").order_by("-created_at")
        serializer = InventoryLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryLogViewSet(ModelViewSet):
    queryset = InventoryLog.objects.select_related("inventory", "created_by")
    serializer_class = InventoryLogSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrWarehouseStaff]
    search_fields = [
        "inventory__product_variant__product_code",
        "type",
        "reference_type",
    ]
    ordering_fields = ["created_at", "quantity", "type"]

    def get_queryset(self):
        queryset = super().get_queryset()

        inventory_id = self.request.query_params.get("inventory")
        operation_type = self.request.query_params.get("type")
        reference_type = self.request.query_params.get("reference_type")

        if inventory_id:
            queryset = queryset.filter(inventory_id=inventory_id)
        if operation_type:
            queryset = queryset.filter(type=operation_type)
        if reference_type:
            queryset = queryset.filter(reference_type=reference_type)

        return queryset.order_by("-created_at")
