from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal

from .models import *


class B2CCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2CCustomer
        fields = "__all__"


class B2CSaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2CSaleItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value


class B2CSaleSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )
    payment_method = serializers.CharField(required=False, default="cash")
    items = B2CSaleItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = B2CSale
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]
        extra_kwargs = {"customer": {"required": False}}


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


class B2CReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2CReturnItem
        fields = "__all__"

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        sale_item = attrs.get("sale_item")
        refund_amount = attrs.get("refund_amount")

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than zero"})
        if refund_amount <= 0:
            raise serializers.ValidationError({"refund_amount": "Refund amount must be greater than zero"})

        returned = B2CReturnItem.objects.filter(
            sale_item=sale_item
        ).aggregate(total=Sum("quantity"))["total"] or 0

        if returned + quantity > sale_item.quantity:
            raise serializers.ValidationError(
                {"quantity": "Returned quantity cannot exceed sold quantity"}
            )

        return attrs


class B2CReturnSerializer(serializers.ModelSerializer):
    total_refund = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )
    items = B2CReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = B2CReturn
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]
