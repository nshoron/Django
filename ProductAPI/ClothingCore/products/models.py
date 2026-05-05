from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='products',
    )
    brand = models.ForeignKey(
        'brands.Brand',
        on_delete=models.PROTECT,
        related_name='products',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    regular_price=models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.alt_text or f'Image {self.pk}'


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
    )
    size = models.ForeignKey(
        'sizes.Size',
        on_delete=models.PROTECT,
        related_name='product_variants',
    )
    color = models.ForeignKey(
        'colors.Color',
        on_delete=models.PROTECT,
        related_name='product_variants',
    )
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size', 'color'],
                name='unique_product_size_color',
            ),
        ]

    def __str__(self):
        return f'{self.product.name} — {self.size.name} / {self.color.name}'
