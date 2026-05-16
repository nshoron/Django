from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError

from .models import Payment, PaymentTransaction
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentTransactionSerializer,
    PaymentTransactionCreateSerializer
)
from .services import (
    create_payment,
    process_payment_transaction,
    process_refund,
    get_payment_status_summary
)
from core.permissions import IsAdminOrManager


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.select_related("invoice", "bill", "created_by")
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['id', 'payment_type']
    ordering_fields = ['created_at', 'total_amount', 'payment_status']
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PaymentSerializer
        return PaymentCreateSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.instance = create_payment(
                invoice=serializer.validated_data.get("invoice"),
                bill=serializer.validated_data.get("bill"),
                payment_type=serializer.validated_data.get("payment_type", "invoice"),
                total_amount=serializer.validated_data.get("total_amount"),
                created_by=self.request.user,
            )
        except ValueError as exc:
            raise ValidationError(str(exc))

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        payment_type = self.request.query_params.get("payment_type")
        invoice_id = self.request.query_params.get("invoice")
        bill_id = self.request.query_params.get("bill")

        if status_value:
            queryset = queryset.filter(payment_status=status_value)
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        if bill_id:
            queryset = queryset.filter(bill_id=bill_id)

        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get payment status summary"""
        summary = get_payment_status_summary()
        return Response(summary, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def due_amount(self, request, pk=None):
        """Get due amount for a payment"""
        payment = self.get_object()
        return Response({
            'payment_id': payment.id,
            'total_amount': payment.total_amount,
            'paid_amount': payment.paid_amount,
            'due_amount': payment.due_amount,
            'status': payment.payment_status
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def partial_payment(self, request, pk=None):
        """Process partial payment"""
        payment = self.get_object()
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method', 'cash')
        transaction_number = request.data.get('transaction_number')
        notes = request.data.get('notes')
        
        if not amount:
            return Response(
                {'error': 'amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            amount = Decimal(str(amount))
            process_payment_transaction(
                payment=payment,
                amount=amount,
                transaction_type='payment',
                payment_method=payment_method,
                transaction_number=transaction_number,
                notes=notes,
                created_by=request.user
            )
            return Response(
                {'message': 'Payment processed successfully'},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def full_payment(self, request, pk=None):
        """Process full payment"""
        payment = self.get_object()
        payment_method = request.data.get('payment_method', 'cash')
        transaction_number = request.data.get('transaction_number')
        notes = request.data.get('notes')
        
        try:
            process_payment_transaction(
                payment=payment,
                amount=payment.due_amount,
                transaction_type='payment',
                payment_method=payment_method,
                transaction_number=transaction_number,
                notes=notes or 'Full payment',
                created_by=request.user
            )
            return Response(
                {'message': 'Full payment processed successfully'},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Process refund"""
        payment = self.get_object()
        refund_amount = request.data.get('refund_amount')
        reason = request.data.get('reason')
        payment_method = request.data.get('payment_method')
        
        if not refund_amount or not reason:
            return Response(
                {'error': 'refund_amount and reason are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            refund_amount = Decimal(str(refund_amount))
            process_refund(
                payment=payment,
                refund_amount=refund_amount,
                reason=reason,
                payment_method=payment_method,
                created_by=request.user
            )
            return Response(
                {'message': 'Refund processed successfully'},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentTransactionViewSet(ModelViewSet):
    queryset = PaymentTransaction.objects.select_related("payment", "created_by")
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    search_fields = ['payment__id', 'transaction_type', 'payment_method']
    ordering_fields = ['created_at', 'amount']
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PaymentTransactionSerializer
        return PaymentTransactionCreateSerializer
    
    def perform_create(self, serializer):
        try:
            transaction_type = serializer.validated_data["transaction_type"]
            if transaction_type == "refund":
                serializer.instance = process_refund(
                    payment=serializer.validated_data["payment"],
                    refund_amount=serializer.validated_data["amount"],
                    reason=serializer.validated_data.get("notes") or "Manual refund",
                    payment_method=serializer.validated_data.get("payment_method"),
                    created_by=self.request.user,
                )
            else:
                serializer.instance = process_payment_transaction(
                    payment=serializer.validated_data["payment"],
                    amount=serializer.validated_data["amount"],
                    transaction_type=transaction_type,
                    payment_method=serializer.validated_data["payment_method"],
                    transaction_number=serializer.validated_data.get("transaction_number"),
                    notes=serializer.validated_data.get("notes"),
                    created_by=self.request.user,
                )
        except ValueError as exc:
            raise ValidationError(str(exc))
