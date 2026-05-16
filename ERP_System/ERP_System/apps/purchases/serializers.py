from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal

from .models import *


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value


class PurchaseSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )
    status = serializers.CharField(required=False, default="completed")
    items = PurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class PurchaseReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturnItem
        fields = "__all__"

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        purchase_item = attrs.get("purchase_item")

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than zero"})

        returned = PurchaseReturnItem.objects.filter(
            purchase_item=purchase_item
        ).aggregate(total=Sum("quantity"))["total"] or 0

        if returned + quantity > purchase_item.quantity:
            raise serializers.ValidationError(
                {"quantity": "Returned quantity cannot exceed purchased quantity"}
            )

        return attrs


class PurchaseReturnSerializer(serializers.ModelSerializer):
    items = PurchaseReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PurchaseReturn
        fields = "__all__"
        read_only_fields = ["supplier", "created_by", "created_at"]
