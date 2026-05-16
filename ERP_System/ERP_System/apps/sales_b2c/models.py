from django.db import models


class B2CCustomer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        db_table = "b2c_customers"

    def __str__(self):
        return self.name


class B2CSale(models.Model):
    customer = models.ForeignKey(
        B2CCustomer,
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

    payment_method = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "b2c_sales"


class B2CSaleItem(models.Model):
    sale = models.ForeignKey(
        B2CSale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = "b2c_sale_items"


class Bill(models.Model):
    sale = models.OneToOneField(
        B2CSale,
        on_delete=models.CASCADE
    )

    bill_number = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bills"


class B2CReturn(models.Model):
    sale = models.ForeignKey(
        B2CSale,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    return_reason = models.TextField()

    total_refund = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "b2c_returns"


class B2CReturnItem(models.Model):
    b2c_return = models.ForeignKey(
        B2CReturn,
        on_delete=models.CASCADE,
        related_name="items"
    )

    sale_item = models.ForeignKey(
        B2CSaleItem,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = "b2c_return_items"