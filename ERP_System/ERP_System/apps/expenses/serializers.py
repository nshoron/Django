from rest_framework import serializers
from .models import ExpenseCategory, Expense


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    expense_category = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ['created_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'expense_category',
            'title',
            'description',
            'amount',
            'payment_method'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
