from django.db import transaction

from .models import Inventory, InventoryLog


STOCK_IN_ACTIONS = {"purchase", "b2c_return", "b2b_return"}
STOCK_OUT_ACTIONS = {"purchase_return", "b2c_sale", "b2b_sale"}
ALL_ACTIONS = STOCK_IN_ACTIONS | STOCK_OUT_ACTIONS | {"adjustment"}


def get_or_create_inventory(product_variant, cost_price=0, retail_price=0):
    inventory, _ = Inventory.objects.get_or_create(
        product_variant=product_variant,
        defaults={
            "cost_price": cost_price,
            "retail_price": retail_price,
            "stock_quantity": 0,
        },
    )
    return inventory


def update_inventory(
    inventory,
    quantity,
    action,
    user,
    reference_id=None,
    reference_type=None
):
    if action not in ALL_ACTIONS:
        raise ValueError("Invalid inventory action")

    if user is None or not getattr(user, "is_authenticated", False):
        raise ValueError("Authenticated user is required")

    quantity = int(quantity)
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    with transaction.atomic():
        inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
        previous = inventory.stock_quantity

        if action in STOCK_IN_ACTIONS:
            inventory.stock_quantity += quantity

        elif action in STOCK_OUT_ACTIONS:
            if inventory.stock_quantity < quantity:
                raise ValueError("Insufficient stock")

            inventory.stock_quantity -= quantity

        elif action == "adjustment":
            inventory.stock_quantity = quantity

        if inventory.stock_quantity < 0:
            raise ValueError("Stock cannot be negative")

        inventory.save(update_fields=["stock_quantity"])

        InventoryLog.objects.create(
            inventory=inventory,
            created_by=user,
            type=action,
            quantity=quantity,
            previous_stock=previous,
            new_stock=inventory.stock_quantity,
            reference_id=reference_id,
            reference_type=reference_type
        )

    return inventory
