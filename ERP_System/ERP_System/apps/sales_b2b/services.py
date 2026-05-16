from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

from apps.inventory.services import get_or_create_inventory, update_inventory
from apps.accounting.services import record_sale_accounting, reverse_sale_accounting
from .models import Invoice


def refresh_b2b_sale_total(sale):
    total = Decimal("0.00")
    for item in sale.items.all():
        total += Decimal(item.quantity) * item.unit_price

    sale.total_amount = total
    sale.save(update_fields=["total_amount"])
    return sale


def process_b2b_sale_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.product_variant
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="b2b_sale",
        user=user,
        reference_id=item.id,
        reference_type="b2b_sale_item"
    )
    refresh_b2b_sale_total(item.b2b_sale)
    record_sale_accounting(item, sale_type="b2b", created_by=user)


def process_b2b_return_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.b2b_sale_item.product_variant
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="b2b_return",
        user=user,
        reference_id=item.id,
        reference_type="b2b_return_item"
    )
    reverse_sale_accounting(item, sale_type="b2b", created_by=user)


def generate_invoice(sale):
    Invoice.objects.get_or_create(
        b2b_sale=sale,
        defaults={
            "invoice_number": f"INV-{sale.id}",
            "due_date": timezone.now() + timedelta(days=30),
            "payment_terms": "Net 30",
            "status": "pending",
        },
    )
