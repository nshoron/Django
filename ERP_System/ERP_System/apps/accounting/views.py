from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import LedgerAccount, AccountingTransaction
from .serializers import (
    LedgerAccountSerializer,
    AccountingTransactionSerializer,
    AccountingTransactionCreateSerializer,
    TrialBalanceSerializer,
    ProfitLossSerializer
)
from .services import (
    create_accounting_entry,
    create_ledger_account,
    get_account_balance,
    get_trial_balance,
    get_profit_loss_report,
    get_account_statement
)
from core.permissions import IsAdminOrManager


class LedgerAccountViewSet(ModelViewSet):
    queryset = LedgerAccount.objects.all()
    serializer_class = LedgerAccountSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['account_name', 'account_type']
    ordering_fields = ['account_name', 'current_balance']

    def perform_create(self, serializer):
        serializer.instance = create_ledger_account(
            account_name=serializer.validated_data["account_name"],
            account_type=serializer.validated_data["account_type"],
            opening_balance=serializer.validated_data["opening_balance"],
        )
    
    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        """Get account balance"""
        account = self.get_object()
        return Response({
            'account_id': account.id,
            'account_name': account.account_name,
            'account_type': account.account_type,
            'balance': account.current_balance
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        """Get account statement"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        statement = get_account_statement(pk, start_date, end_date)
        
        if not statement:
            return Response(
                {'error': 'Account not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(statement, status=status.HTTP_200_OK)


class AccountingTransactionViewSet(ModelViewSet):
    queryset = AccountingTransaction.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['ledger_account__account_name', 'entry_type', 'description']
    ordering_fields = ['created_at', 'amount']
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AccountingTransactionSerializer
        return AccountingTransactionCreateSerializer
    
    def perform_create(self, serializer):
        serializer.instance = create_accounting_entry(
            ledger_account=serializer.validated_data["ledger_account"],
            entry_type=serializer.validated_data["entry_type"],
            amount=serializer.validated_data["amount"],
            description=serializer.validated_data.get("description"),
            created_by=self.request.user,
            b2b_sale=serializer.validated_data.get("b2b_sale"),
            b2c_sale=serializer.validated_data.get("b2c_sale"),
            purchase=serializer.validated_data.get("purchase"),
            expense=serializer.validated_data.get("expense"),
            payment=serializer.validated_data.get("payment"),
        )
    
    @action(detail=False, methods=['get'])
    def trial_balance(self, request):
        """Get trial balance"""
        trial_balance = get_trial_balance()
        
        data = []
        for account_name, balances in trial_balance.items():
            data.append({
                'account_name': account_name,
                'debit': balances['debit'],
                'credit': balances['credit'],
                'balance': balances['balance']
            })
        
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def profit_loss(self, request):
        """Get profit/loss report"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        report = get_profit_loss_report(start_date, end_date)
        return Response(report, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def ledger_by_type(self, request):
        """Get transactions by account type"""
        account_type = request.query_params.get('account_type')
        
        if not account_type:
            return Response(
                {'error': 'account_type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        accounts = LedgerAccount.objects.filter(account_type=account_type)
        transactions = AccountingTransaction.objects.filter(
            ledger_account__in=accounts
        ).order_by('-created_at')
        
        serializer = AccountingTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
