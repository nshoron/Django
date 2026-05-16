from django.db import models


class Inventory(models.Model):
    product_variant = models.OneToOneField(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity = models.IntegerField(default=0)

    reorder_level = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory"

    def __str__(self):
        return self.product_variant.product_code


class InventoryLog(models.Model):
    TYPE_CHOICES = [
        ("purchase", "Purchase"),
        ("purchase_return", "Purchase Return"),
        ("b2c_sale", "B2C Sale"),
        ("b2c_return", "B2C Return"),
        ("b2b_sale", "B2B Sale"),
        ("b2b_return", "B2B Return"),
        ("adjustment", "Adjustment"),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    reference_id = models.IntegerField(
        null=True,
        blank=True
    )

    reference_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    quantity = models.IntegerField()

    previous_stock = models.IntegerField()

    new_stock = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_logs"

    def __str__(self):
        return f"{self.inventory} - {self.type}"