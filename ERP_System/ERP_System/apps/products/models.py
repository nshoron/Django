from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "sizes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color_code = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.color_code})"


class Product(models.Model):
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        related_name="products"
    )

    brand = models.ForeignKey(
        "products.Brand",
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)

    class Meta:
        db_table = "products"
        ordering = ["name"]
        unique_together = ["category", "brand", "name"]

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    
    product_code = models.CharField(
        max_length=100,
        unique=True
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="variants"
    )

    size = models.ForeignKey(
        "products.Size",
        on_delete=models.CASCADE
    )

    color = models.ForeignKey(
        "products.Color",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "product_variants"
        unique_together = ["product", "size", "color"]

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"