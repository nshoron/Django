from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from .models import Expense, ExpenseCategory
from apps.accounting.services import parse_datetime_value, record_expense_accounting


def create_expense(category_id, title, amount, payment_method, description=None, created_by=None):
    """Create an expense and create corresponding accounting entry"""
    try:
        category = ExpenseCategory.objects.get(id=category_id)
    except ExpenseCategory.DoesNotExist:
        raise ValueError(f"Expense category with id {category_id} does not exist")
    
    expense = Expense.objects.create(
        expense_category=category,
        title=title,
        description=description,
        amount=amount,
        payment_method=payment_method,
        created_by=created_by
    )
    
    record_expense_accounting(expense, created_by=created_by)
    
    return expense


def get_expense_summary(start_date=None, end_date=None):
    """Get expense summary by category"""
    start_date = parse_datetime_value(start_date, timezone.now().replace(month=1, day=1))
    end_date = parse_datetime_value(end_date, timezone.now())
    
    categories = ExpenseCategory.objects.all()
    summary = {}
    total_expenses = Decimal('0.00')
    
    for category in categories:
        category_total = Expense.objects.filter(
            expense_category=category,
            created_at__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        summary[category.name] = {
            'total': category_total,
            'count': Expense.objects.filter(
                expense_category=category,
                created_at__range=[start_date, end_date]
            ).count()
        }
        total_expenses += category_total
    
    summary['total_all'] = total_expenses
    summary['period_start'] = start_date
    summary['period_end'] = end_date
    
    return summary


def get_monthly_expenses(year=None, month=None):
    """Get expenses for a specific month"""
    from datetime import datetime, timedelta
    
    if not year:
        year = timezone.now().year
    if not month:
        month = timezone.now().month
    
    start_date = timezone.make_aware(datetime(year, month, 1))
    if month == 12:
        end_date = timezone.make_aware(datetime(year + 1, 1, 1))
    else:
        end_date = timezone.make_aware(datetime(year, month + 1, 1))
    
    expenses = Expense.objects.filter(
        created_at__range=[start_date, end_date]
    ).order_by('-created_at')
    
    total = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    return {
        'month': month,
        'year': year,
        'expenses': expenses,
        'total': total
    }
