from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError

from .models import ExpenseCategory, Expense
from .serializers import (
    ExpenseCategorySerializer,
    ExpenseSerializer,
    ExpenseCreateSerializer
)
from .services import (
    create_expense,
    get_expense_summary,
    get_monthly_expenses
)
from core.permissions import IsAdminOrManager


class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['name']
    ordering_fields = ['name']


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.select_related("expense_category", "created_by")
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['title', 'description', 'expense_category__name']
    ordering_fields = ['created_at', 'amount']
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ExpenseSerializer
        return ExpenseCreateSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.instance = create_expense(
                category_id=serializer.validated_data["expense_category"].id,
                title=serializer.validated_data["title"],
                amount=serializer.validated_data["amount"],
                payment_method=serializer.validated_data["payment_method"],
                description=serializer.validated_data.get("description"),
                created_by=self.request.user,
            )
        except ValueError as exc:
            raise ValidationError(str(exc))

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        payment_method = self.request.query_params.get("payment_method")

        if category_id:
            queryset = queryset.filter(expense_category_id=category_id)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get expense summary"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        summary = get_expense_summary(start_date, end_date)
        return Response(summary, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly expenses"""
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        
        if year:
            year = int(year)
        if month:
            month = int(month)
        
        expenses_data = get_monthly_expenses(year, month)
        
        data = {
            'month': expenses_data['month'],
            'year': expenses_data['year'],
            'total': expenses_data['total'],
            'expenses': ExpenseSerializer(
                expenses_data['expenses'],
                many=True
            ).data
        }
        
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="by-payment-method")
    def by_payment_method(self, request):
        payment_method = request.query_params.get('payment_method')
        if not payment_method:
            return Response(
                {'error': 'payment_method is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        expenses = self.filter_queryset(self.get_queryset().filter(payment_method=payment_method))
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
