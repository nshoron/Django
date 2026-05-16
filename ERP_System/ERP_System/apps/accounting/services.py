from decimal import Decimal
from datetime import datetime, time
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from .models import LedgerAccount, AccountingTransaction


def to_decimal(value):
    return Decimal(str(value))


def parse_datetime_value(value, default):
    if not value:
        return default

    parsed = parse_datetime(value)
    if parsed is None:
        parsed_date = parse_date(value)
        if parsed_date:
            parsed = datetime.combine(parsed_date, time.min)

    if parsed is None:
        return default

    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)

    return parsed


def get_ledger_account(account_type):
    return LedgerAccount.objects.filter(account_type=account_type).first()


def payment_ledger_type(payment_method):
    if payment_method in {"bank", "bank_transfer", "card", "mobile_banking"}:
        return "bank"
    return "cash"


def create_accounting_entry(ledger_account, entry_type, amount, description=None, created_by=None, 
                           b2b_sale=None, b2c_sale=None, purchase=None, expense=None, payment=None):
    """Create an accounting transaction entry"""
    if entry_type not in {"debit", "credit"}:
        raise ValueError("entry_type must be debit or credit")

    amount = to_decimal(amount)
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    with transaction.atomic():
        ledger_account = LedgerAccount.objects.select_for_update().get(pk=ledger_account.pk)

        transaction_obj = AccountingTransaction.objects.create(
            ledger_account=ledger_account,
            entry_type=entry_type,
            amount=amount,
            description=description or f"{entry_type.capitalize()} entry",
            created_by=created_by,
            b2b_sale=b2b_sale,
            b2c_sale=b2c_sale,
            purchase=purchase,
            expense=expense,
            payment=payment
        )

        if entry_type == "debit":
            ledger_account.current_balance += amount
        else:
            ledger_account.current_balance -= amount

        ledger_account.save(update_fields=["current_balance"])

    return transaction_obj


def create_entry_if_account(account_type, entry_type, amount, description=None, created_by=None, **references):
    account = get_ledger_account(account_type)
    if not account:
        return None

    return create_accounting_entry(
        ledger_account=account,
        entry_type=entry_type,
        amount=amount,
        description=description,
        created_by=created_by,
        **references,
    )


def record_purchase_accounting(purchase_item, created_by=None):
    amount = to_decimal(purchase_item.quantity) * purchase_item.unit_cost
    purchase = purchase_item.purchase

    create_entry_if_account(
        "inventory",
        "debit",
        amount,
        f"Inventory purchased for Purchase #{purchase.id}",
        created_by=created_by,
        purchase=purchase,
    )
    create_entry_if_account(
        "cash",
        "credit",
        amount,
        f"Purchase payment for Purchase #{purchase.id}",
        created_by=created_by,
        purchase=purchase,
    )


def record_sale_accounting(sale_item, sale_type, created_by=None):
    amount = to_decimal(sale_item.quantity) * sale_item.unit_price
    references = {}

    if sale_type == "b2c":
        references["b2c_sale"] = sale_item.sale
        description_ref = f"B2C Sale #{sale_item.sale_id}"
    else:
        references["b2b_sale"] = sale_item.b2b_sale
        description_ref = f"B2B Sale #{sale_item.b2b_sale_id}"

    create_entry_if_account(
        "sales revenue",
        "credit",
        amount,
        f"Revenue from {description_ref}",
        created_by=created_by,
        **references,
    )

    receivable = get_ledger_account("accounts receivable")
    if receivable:
        create_accounting_entry(
            ledger_account=receivable,
            entry_type="debit",
            amount=amount,
            description=f"Receivable from {description_ref}",
            created_by=created_by,
            **references,
        )


def record_payment_accounting(payment, amount, payment_method, created_by=None):
    account_type = payment_ledger_type(payment_method)
    create_entry_if_account(
        account_type,
        "debit",
        amount,
        f"Payment received for Payment #{payment.id}",
        created_by=created_by,
        payment=payment,
    )

    receivable = get_ledger_account("accounts receivable")
    if receivable:
        create_accounting_entry(
            ledger_account=receivable,
            entry_type="credit",
            amount=amount,
            description=f"Receivable cleared for Payment #{payment.id}",
            created_by=created_by,
            payment=payment,
        )


def record_refund_accounting(payment, amount, payment_method, reason, created_by=None):
    account_type = payment_ledger_type(payment_method)
    create_entry_if_account(
        account_type,
        "credit",
        amount,
        f"Refund for Payment #{payment.id}: {reason}",
        created_by=created_by,
        payment=payment,
    )

    receivable = get_ledger_account("accounts receivable")
    if receivable:
        create_accounting_entry(
            ledger_account=receivable,
            entry_type="debit",
            amount=amount,
            description=f"Receivable reopened for refund Payment #{payment.id}",
            created_by=created_by,
            payment=payment,
        )


def record_expense_accounting(expense, created_by=None):
    create_entry_if_account(
        "expenses",
        "debit",
        expense.amount,
        f"Expense: {expense.title} ({expense.expense_category.name})",
        created_by=created_by,
        expense=expense,
    )
    create_entry_if_account(
        payment_ledger_type(expense.payment_method),
        "credit",
        expense.amount,
        f"Expense payment: {expense.title}",
        created_by=created_by,
        expense=expense,
    )


def reverse_purchase_accounting(purchase_return_item, created_by=None):
    amount = to_decimal(purchase_return_item.quantity) * purchase_return_item.purchase_item.unit_cost
    purchase = purchase_return_item.purchase_return.purchase

    create_entry_if_account(
        "inventory",
        "credit",
        amount,
        f"Inventory returned for Purchase #{purchase.id}",
        created_by=created_by,
        purchase=purchase,
    )
    create_entry_if_account(
        "cash",
        "debit",
        amount,
        f"Supplier refund for Purchase #{purchase.id}",
        created_by=created_by,
        purchase=purchase,
    )


def reverse_sale_accounting(return_item, sale_type, created_by=None):
    if sale_type == "b2c":
        amount = return_item.refund_amount
        references = {"b2c_sale": return_item.b2c_return.sale}
        description_ref = f"B2C Sale #{return_item.b2c_return.sale_id}"
    else:
        amount = to_decimal(return_item.quantity) * return_item.b2b_sale_item.unit_price
        references = {"b2b_sale": return_item.b2b_return.b2b_sale}
        description_ref = f"B2B Sale #{return_item.b2b_return.b2b_sale_id}"

    create_entry_if_account(
        "sales revenue",
        "debit",
        amount,
        f"Revenue reversal for {description_ref}",
        created_by=created_by,
        **references,
    )

    receivable = get_ledger_account("accounts receivable")
    if receivable:
        create_accounting_entry(
            ledger_account=receivable,
            entry_type="credit",
            amount=amount,
            description=f"Receivable reversal for {description_ref}",
            created_by=created_by,
            **references,
        )

def create_ledger_account(account_name, account_type, opening_balance=Decimal('0.00')):
    """Create a new ledger account"""
    account = LedgerAccount.objects.create(
        account_name=account_name,
        account_type=account_type,
        opening_balance=opening_balance,
        current_balance=opening_balance
    )
    return account


def get_account_balance(account_id):
    """Get current balance of an account"""
    try:
        account = LedgerAccount.objects.get(id=account_id)
        return account.current_balance
    except LedgerAccount.DoesNotExist:
        return None


def get_trial_balance():
    """Get trial balance (sum of all debit and credit entries)"""
    accounts = LedgerAccount.objects.all()
    trial_balance = {}
    
    for account in accounts:
        debits = AccountingTransaction.objects.filter(
            ledger_account=account,
            entry_type="debit"
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        credits = AccountingTransaction.objects.filter(
            ledger_account=account,
            entry_type="credit"
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        trial_balance[account.account_name] = {
            'debit': debits,
            'credit': credits,
            'balance': account.current_balance
        }
    
    return trial_balance


def get_profit_loss_report(start_date=None, end_date=None):
    """Generate profit/loss report"""
    start_date = parse_datetime_value(start_date, timezone.now().replace(month=1, day=1))
    end_date = parse_datetime_value(end_date, timezone.now())
    
    # Get revenue accounts
    revenue_accounts = LedgerAccount.objects.filter(account_type="sales revenue")
    revenue = AccountingTransaction.objects.filter(
        ledger_account__in=revenue_accounts,
        created_at__range=[start_date, end_date],
        entry_type="credit"
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Get expense accounts
    expense_accounts = LedgerAccount.objects.filter(account_type="expenses")
    expenses = AccountingTransaction.objects.filter(
        ledger_account__in=expense_accounts,
        created_at__range=[start_date, end_date],
        entry_type="debit"
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    net_profit = revenue - expenses
    
    return {
        'revenue': revenue,
        'expenses': expenses,
        'net_profit': net_profit,
        'period_start': start_date,
        'period_end': end_date
    }


def get_account_statement(account_id, start_date=None, end_date=None):
    """Get account statement with all transactions"""
    start_date = parse_datetime_value(start_date, timezone.now().replace(month=1, day=1))
    end_date = parse_datetime_value(end_date, timezone.now())
    
    try:
        account = LedgerAccount.objects.get(id=account_id)
    except LedgerAccount.DoesNotExist:
        return None
    
    transactions = AccountingTransaction.objects.filter(
        ledger_account=account,
        created_at__range=[start_date, end_date]
    ).order_by('-created_at')
    
    return {
        'account': account.account_name,
        'account_type': account.account_type,
        'opening_balance': account.opening_balance,
        'transactions': [
            {
                "id": transaction.id,
                "entry_type": transaction.entry_type,
                "amount": transaction.amount,
                "description": transaction.description,
                "created_at": transaction.created_at,
            }
            for transaction in transactions
        ],
        'closing_balance': account.current_balance
    }
