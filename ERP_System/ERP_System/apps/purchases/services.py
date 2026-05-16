from decimal import Decimal

from apps.inventory.services import get_or_create_inventory, update_inventory
from apps.accounting.services import record_purchase_accounting, reverse_purchase_accounting


def refresh_purchase_total(purchase):
    total = Decimal("0.00")
    for item in purchase.items.all():
        total += Decimal(item.quantity) * item.unit_cost

    purchase.total_amount = total
    purchase.save(update_fields=["total_amount"])
    return purchase


def process_purchase_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.product_variant,
        cost_price=item.unit_cost,
        retail_price=item.unit_cost,
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="purchase",
        user=user,
        reference_id=item.id,
        reference_type="purchase_item"
    )
    refresh_purchase_total(item.purchase)
    record_purchase_accounting(item, created_by=user)


def process_purchase_return_item(item, user):
    inventory = get_or_create_inventory(
        product_variant=item.purchase_item.product_variant,
        cost_price=item.purchase_item.unit_cost,
        retail_price=item.purchase_item.unit_cost,
    )

    update_inventory(
        inventory=inventory,
        quantity=item.quantity,
        action="purchase_return",
        user=user,
        reference_id=item.id,
        reference_type="purchase_return_item"
    )
    reverse_purchase_accounting(item, created_by=user)
