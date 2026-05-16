from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal

from .models import *


class B2BCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BCustomer
        fields = "__all__"


class B2BSaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BSaleItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value


class B2BSaleSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )
    items = B2BSaleItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = B2BSale
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class InvoiceSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, default="pending")

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["created_at"]


class B2BReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BReturnItem
        fields = "__all__"

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        sale_item = attrs.get("b2b_sale_item")

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than zero"})

        returned = B2BReturnItem.objects.filter(
            b2b_sale_item=sale_item
        ).aggregate(total=Sum("quantity"))["total"] or 0

        if returned + quantity > sale_item.quantity:
            raise serializers.ValidationError(
                {"quantity": "Returned quantity cannot exceed sold quantity"}
            )

        return attrs


class B2BReturnSerializer(serializers.ModelSerializer):
    items = B2BReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = B2BReturn
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]
