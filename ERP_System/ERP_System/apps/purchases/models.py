from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    class Meta:
        db_table = "suppliers"

    def __str__(self):
        return self.name


class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchases"

    def __str__(self):
        return f"Purchase #{self.id}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = "purchase_items"


class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchase_returns"


class PurchaseReturnItem(models.Model):
    purchase_return = models.ForeignKey(
        PurchaseReturn,
        on_delete=models.CASCADE,
        related_name="items"
    )

    purchase_item = models.ForeignKey(
        PurchaseItem,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    class Meta:
        db_table = "purchase_return_items"