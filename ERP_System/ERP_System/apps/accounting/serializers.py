from rest_framework import serializers
from .models import LedgerAccount, AccountingTransaction


class LedgerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerAccount
        fields = "__all__"
        read_only_fields = ['created_at', 'current_balance']


class AccountingTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    ledger_account = serializers.StringRelatedField()
    
    class Meta:
        model = AccountingTransaction
        fields = "__all__"
        read_only_fields = ['created_at']


class AccountingTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingTransaction
        fields = [
            'ledger_account',
            'entry_type',
            'amount',
            'description',
            'b2b_sale',
            'b2c_sale',
            'purchase',
            'expense',
            'payment'
        ]


class LedgerAccountBalanceSerializer(serializers.Serializer):
    """Serializer for ledger account balance"""
    account_id = serializers.IntegerField()
    account_name = serializers.CharField()
    account_type = serializers.CharField()
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class TrialBalanceSerializer(serializers.Serializer):
    """Serializer for trial balance"""
    account_name = serializers.CharField()
    debit = serializers.DecimalField(max_digits=12, decimal_places=2)
    credit = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class ProfitLossSerializer(serializers.Serializer):
    """Serializer for profit/loss report"""
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    period_start = serializers.DateTimeField()
    period_end = serializers.DateTimeField()
