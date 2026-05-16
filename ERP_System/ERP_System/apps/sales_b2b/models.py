from django.db import models


class B2BCustomer(models.Model):
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    tax_id = models.CharField(max_length=100)

    class Meta:
        db_table = "b2b_customers"

    def __str__(self):
        return self.company_name


class B2BSale(models.Model):
    b2b_customer = models.ForeignKey(
        B2BCustomer,
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

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "b2b_sales"


class B2BSaleItem(models.Model):
    b2b_sale = models.ForeignKey(
        B2BSale,
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
        db_table = "b2b_sale_items"


class Invoice(models.Model):
    b2b_sale = models.OneToOneField(
        B2BSale,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    due_date = models.DateTimeField()

    payment_terms = models.CharField(max_length=100)

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"


class B2BReturn(models.Model):
    b2b_sale = models.ForeignKey(
        B2BSale,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    return_reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "b2b_returns"


class B2BReturnItem(models.Model):
    b2b_return = models.ForeignKey(
        B2BReturn,
        on_delete=models.CASCADE,
        related_name="items"
    )

    b2b_sale_item = models.ForeignKey(
        B2BSaleItem,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    class Meta:
        db_table = "b2b_return_items"