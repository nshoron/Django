from decimal import Decimal
from django.db import transaction

from apps.accounting.services import record_payment_accounting, record_refund_accounting
from .models import Payment, PaymentTransaction


def sync_invoice_status(payment):
    if payment.invoice:
        payment.invoice.status = payment.payment_status
        payment.invoice.save(update_fields=["status"])


def update_payment_status(payment):
    if payment.due_amount == 0:
        payment.payment_status = "paid"
    elif payment.paid_amount > 0:
        payment.payment_status = "partial"
    else:
        payment.payment_status = "pending"


def create_payment(invoice=None, bill=None, total_amount=None, payment_type="invoice", created_by=None):
    """Create a payment record for invoice or bill"""
    if bool(invoice) == bool(bill):
        raise ValueError("Provide either invoice or bill, not both")
    
    if total_amount is None:
        if invoice:
            total_amount = invoice.b2b_sale.total_amount
        else:
            total_amount = bill.sale.total_amount

    total_amount = Decimal(str(total_amount))
    if total_amount < 0:
        raise ValueError("total_amount cannot be negative")
    
    payment = Payment.objects.create(
        invoice=invoice,
        bill=bill,
        payment_type=payment_type,
        total_amount=total_amount,
        paid_amount=Decimal('0.00'),
        due_amount=total_amount,
        payment_status="pending",
        created_by=created_by
    )
    
    return payment


def process_payment_transaction(payment, amount, transaction_type, payment_method, transaction_number=None, notes=None, created_by=None):
    amount = Decimal(str(amount))
    if transaction_type != "payment":
        raise ValueError("transaction_type must be payment")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    with transaction.atomic():
        payment = Payment.objects.select_for_update().get(pk=payment.pk)
        if amount > payment.due_amount:
            raise ValueError(f"Payment amount cannot exceed due amount of {payment.due_amount}")

        transaction_obj = PaymentTransaction.objects.create(
            payment=payment,
            amount=amount,
            transaction_type=transaction_type,
            payment_method=payment_method,
            transaction_number=transaction_number,
            notes=notes,
            created_by=created_by
        )

        payment.paid_amount += amount
        payment.due_amount -= amount
        update_payment_status(payment)
        payment.save(update_fields=["paid_amount", "due_amount", "payment_status"])
        sync_invoice_status(payment)

    record_payment_accounting(
        payment=payment,
        amount=amount,
        payment_method=payment_method,
        created_by=created_by,
    )

    return transaction_obj


def process_refund(payment, refund_amount, reason, payment_method=None, created_by=None):
    """Process a refund for a payment"""
    refund_amount = Decimal(str(refund_amount))
    if refund_amount <= 0:
        raise ValueError("refund_amount must be greater than zero")

    with transaction.atomic():
        payment = Payment.objects.select_for_update().get(pk=payment.pk)
        if refund_amount > payment.paid_amount:
            raise ValueError(f"Refund amount cannot exceed paid amount of {payment.paid_amount}")

        payment_method = (
            payment_method
            or payment.paymenttransaction_set.order_by("-created_at").values_list("payment_method", flat=True).first()
            or "cash"
        )

        transaction_obj = PaymentTransaction.objects.create(
            payment=payment,
            amount=refund_amount,
            transaction_type="refund",
            payment_method=payment_method,
            notes=f"Refund: {reason}",
            created_by=created_by
        )

        payment.paid_amount -= refund_amount
        payment.due_amount += refund_amount

        if payment.paid_amount == 0:
            payment.payment_status = "refunded"
        elif payment.due_amount > 0:
            payment.payment_status = "partial"
        else:
            payment.payment_status = "paid"

        payment.save(update_fields=["paid_amount", "due_amount", "payment_status"])
        sync_invoice_status(payment)

    record_refund_accounting(
        payment=payment,
        amount=refund_amount,
        payment_method=payment_method,
        reason=reason,
        created_by=created_by,
    )

    return transaction_obj


def get_payment_status_summary():
    """Get summary of all payments by status"""
    from django.db.models import Sum
    
    return {
        'total_receivable': Payment.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_paid': Payment.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0,
        'total_due': Payment.objects.aggregate(Sum('due_amount'))['due_amount__sum'] or 0,
        'pending': Payment.objects.filter(payment_status='pending').count(),
        'partial': Payment.objects.filter(payment_status='partial').count(),
        'paid': Payment.objects.filter(payment_status='paid').count(),
        'refunded': Payment.objects.filter(payment_status='refunded').count(),
    }
