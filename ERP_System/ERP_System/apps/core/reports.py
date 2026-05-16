from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Count
from decimal import Decimal

from apps.inventory.models import Inventory, InventoryLog
from apps.purchases.models import Purchase, PurchaseItem, Supplier
from apps.sales_b2c.models import B2CCustomer, B2CSale, B2CSaleItem
from apps.sales_b2b.models import B2BCustomer, B2BSale, B2BSaleItem
from apps.payments.models import Payment
from apps.expenses.models import Expense
from apps.products.models import Product
from apps.accounting.services import get_profit_loss_report


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """Get dashboard summary with key metrics"""
    
    # Inventory metrics
    total_products = Product.objects.count()
    total_stock = Inventory.objects.aggregate(Sum('stock_quantity'))['stock_quantity__sum'] or 0
    low_stock_count = Inventory.objects.filter(stock_quantity__lte=10).count()
    
    # Sales metrics
    b2c_sales_total = B2CSale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    b2b_sales_total = B2BSale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    total_sales = b2c_sales_total + b2b_sales_total
    
    # Purchase metrics
    total_purchases = Purchase.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    
    # Expense metrics
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Payment metrics
    total_receivable = Payment.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    total_received = Payment.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or Decimal('0.00')
    
    # Net profit calculation (simplified)
    net_profit = total_sales - total_purchases - total_expenses
    
    return Response({
        'summary': {
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock_count': low_stock_count,
            'total_sales': total_sales,
            'b2c_sales': b2c_sales_total,
            'b2b_sales': b2b_sales_total,
            'total_purchases': total_purchases,
            'total_expenses': total_expenses,
            'total_receivable': total_receivable,
            'total_received': total_received,
            'net_profit': net_profit,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_report(request):
    """Get inventory report"""
    
    inventory_items = Inventory.objects.all().select_related('product_variant')
    
    data = {
        'total_items': inventory_items.count(),
        'total_stock_value': Decimal('0.00'),
        'low_stock_items': [],
        'out_of_stock_items': [],
        'inventory_details': []
    }
    
    for item in inventory_items:
        stock_value = (item.stock_quantity * item.cost_price)
        data['total_stock_value'] += stock_value
        
        item_data = {
            'product_code': item.product_variant.product_code,
            'product': str(item.product_variant.product),
            'size': str(item.product_variant.size),
            'color': str(item.product_variant.color),
            'stock_quantity': item.stock_quantity,
            'cost_price': item.cost_price,
            'retail_price': item.retail_price,
            'stock_value': stock_value,
            'reorder_level': item.reorder_level,
        }
        data['inventory_details'].append(item_data)
        
        if item.stock_quantity <= 0:
            data['out_of_stock_items'].append(item_data)
        elif item.stock_quantity <= item.reorder_level:
            data['low_stock_items'].append(item_data)
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def low_stock_report(request):
    """Get low stock and out of stock items"""
    inventory_items = Inventory.objects.select_related(
        'product_variant',
        'product_variant__product',
        'product_variant__size',
        'product_variant__color',
    )

    low_stock_items = []
    out_of_stock_items = []

    for item in inventory_items:
        item_data = {
            'inventory_id': item.id,
            'product_code': item.product_variant.product_code,
            'product': str(item.product_variant.product),
            'size': str(item.product_variant.size),
            'color': str(item.product_variant.color),
            'stock_quantity': item.stock_quantity,
            'reorder_level': item.reorder_level,
        }

        if item.stock_quantity <= 0:
            out_of_stock_items.append(item_data)
        elif item.stock_quantity <= item.reorder_level:
            low_stock_items.append(item_data)

    return Response({
        'low_stock_count': len(low_stock_items),
        'out_of_stock_count': len(out_of_stock_items),
        'low_stock_items': low_stock_items,
        'out_of_stock_items': out_of_stock_items,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_report(request):
    """Get sales report"""
    
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    b2c_sales = B2CSale.objects.all()
    b2b_sales = B2BSale.objects.all()
    
    if start_date:
        from django.utils import timezone
        from datetime import datetime
        start = timezone.make_aware(datetime.fromisoformat(start_date))
        b2c_sales = b2c_sales.filter(created_at__gte=start)
        b2b_sales = b2b_sales.filter(created_at__gte=start)
    
    if end_date:
        from django.utils import timezone
        from datetime import datetime
        end = timezone.make_aware(datetime.fromisoformat(end_date))
        b2c_sales = b2c_sales.filter(created_at__lte=end)
        b2b_sales = b2b_sales.filter(created_at__lte=end)
    
    b2c_total = b2c_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    b2b_total = b2b_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    
    return Response({
        'b2c_sales': {
            'count': b2c_sales.count(),
            'total_amount': b2c_total
        },
        'b2b_sales': {
            'count': b2b_sales.count(),
            'total_amount': b2b_total
        },
        'total_sales': b2c_total + b2b_total
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_report(request):
    """Get purchase report"""
    
    purchases = Purchase.objects.all().select_related('supplier')
    
    supplier_purchases = {}
    total_amount = Decimal('0.00')
    
    for purchase in purchases:
        supplier_name = purchase.supplier.name
        if supplier_name not in supplier_purchases:
            supplier_purchases[supplier_name] = {
                'count': 0,
                'total_amount': Decimal('0.00')
            }
        supplier_purchases[supplier_name]['count'] += 1
        supplier_purchases[supplier_name]['total_amount'] += purchase.total_amount
        total_amount += purchase.total_amount
    
    return Response({
        'total_purchases': purchases.count(),
        'total_amount': total_amount,
        'by_supplier': supplier_purchases
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_report(request):
    """Get supplier-wise purchase report"""
    data = []

    for supplier in Supplier.objects.all():
        purchases = Purchase.objects.filter(supplier=supplier)
        data.append({
            'supplier_id': supplier.id,
            'supplier': supplier.name,
            'phone': supplier.phone,
            'email': supplier.email,
            'purchase_count': purchases.count(),
            'total_amount': purchases.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00'),
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_report(request):
    """Get B2C and B2B customer sales summary"""
    b2c_customers = []
    for customer in B2CCustomer.objects.all():
        sales = B2CSale.objects.filter(customer=customer)
        b2c_customers.append({
            'customer_id': customer.id,
            'name': customer.name,
            'phone': customer.phone,
            'sale_count': sales.count(),
            'total_amount': sales.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00'),
        })

    b2b_customers = []
    for customer in B2BCustomer.objects.all():
        sales = B2BSale.objects.filter(b2b_customer=customer)
        b2b_customers.append({
            'customer_id': customer.id,
            'company_name': customer.company_name,
            'contact_name': customer.contact_name,
            'phone': customer.phone,
            'sale_count': sales.count(),
            'total_amount': sales.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00'),
        })

    return Response({
        'b2c_customers': b2c_customers,
        'b2b_customers': b2b_customers,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_report(request):
    """Get payment report"""
    
    payments = Payment.objects.all()
    
    payment_status_summary = {
        'pending': payments.filter(payment_status='pending').aggregate(Sum('due_amount'))['due_amount__sum'] or Decimal('0.00'),
        'partial': payments.filter(payment_status='partial').count(),
        'paid': payments.filter(payment_status='paid').count(),
    }
    
    return Response({
        'total_payments': payments.count(),
        'total_receivable': payments.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00'),
        'total_received': payments.aggregate(Sum('paid_amount'))['paid_amount__sum'] or Decimal('0.00'),
        'total_pending': payments.aggregate(Sum('due_amount'))['due_amount__sum'] or Decimal('0.00'),
        'status_summary': payment_status_summary
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_report(request):
    """Get expense report"""
    
    expenses = Expense.objects.all().select_related('expense_category')
    
    by_category = {}
    total_expenses = Decimal('0.00')
    
    for expense in expenses:
        category_name = expense.expense_category.name
        if category_name not in by_category:
            by_category[category_name] = Decimal('0.00')
        by_category[category_name] += expense.amount
        total_expenses += expense.amount
    
    return Response({
        'total_expenses': expenses.count(),
        'total_amount': total_expenses,
        'by_category': by_category
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profit_loss_report(request):
    """Get profit/loss report"""
    report = get_profit_loss_report(
        start_date=request.query_params.get('start_date'),
        end_date=request.query_params.get('end_date'),
    )
    return Response(report, status=status.HTTP_200_OK)
