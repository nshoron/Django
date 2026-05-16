from decimal import Decimal

from apps.inventory.services import get_or_create_inventory, update_inventory
from apps.accounting.services import record_sale_accounting, reverse_sale_accounting
from .models import Bill


def refresh_sale_total(sale):
    total = Decimal("0.00")
    for item in sale.items.all():
        total += Decimal(item.quantity) * item.unit_price

    sale.total_amount = total
    sale.save(update_fields=["total_amount"])
    return sale


def refresh_return_total(b2c_return):
    total = Decimal("0.00")
    for item in b2c_return.items.all():
        total += item.refund_amount

    b2c_return.total_refund = total
    b2c_return.save(update_fields=["total_refund"])
    return b2c_return


def process_sale_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.product_variant
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="b2c_sale",
        user=user,
        reference_id=item.id,
        reference_type="b2c_sale_item"
    )
    refresh_sale_total(item.sale)
    record_sale_accounting(item, sale_type="b2c", created_by=user)


def process_return_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.sale_item.product_variant
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="b2c_return",
        user=user,
        reference_id=item.id,
        reference_type="b2c_return_item"
    )
    refresh_return_total(item.b2c_return)
    reverse_sale_accounting(item, sale_type="b2c", created_by=user)


def generate_bill(sale):
    Bill.objects.get_or_create(
        sale=sale,
        defaults={"bill_number": f"BILL-{sale.id}"}
    )
