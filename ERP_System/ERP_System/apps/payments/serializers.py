from rest_framework import serializers
from decimal import Decimal

from .models import Payment, PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = PaymentTransaction
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    transactions = PaymentTransactionSerializer(
        source='paymenttransaction_set',
        many=True,
        read_only=True
    )
    created_by = serializers.StringRelatedField()
    invoice = serializers.StringRelatedField()
    bill = serializers.StringRelatedField()
    
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            'paid_amount',
            'due_amount',
            'payment_status',
            'created_at'
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Payment
        fields = [
            'invoice',
            'bill',
            'payment_type',
            'total_amount'
        ]

    def validate(self, attrs):
        invoice = attrs.get("invoice")
        bill = attrs.get("bill")
        total_amount = attrs.get("total_amount")

        if bool(invoice) == bool(bill):
            raise serializers.ValidationError("Provide either invoice or bill, not both")
        if total_amount is not None and total_amount < Decimal("0.00"):
            raise serializers.ValidationError({"total_amount": "Total amount cannot be negative"})

        return attrs


class PaymentTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'payment',
            'amount',
            'transaction_type',
            'payment_method',
            'transaction_number',
            'notes'
        ]

    def validate(self, attrs):
        amount = attrs.get("amount")
        transaction_type = attrs.get("transaction_type")

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than zero"})
        if transaction_type not in {"payment", "refund"}:
            raise serializers.ValidationError(
                {"transaction_type": "Transaction type must be payment or refund"}
            )

        return attrs
