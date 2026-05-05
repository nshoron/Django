from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        ordering =['id']
    def __str__(self):
        return f'cart #{self.pk}'


class CartItem(models.Model):
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_varient=models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f'{self.quantity}× variant {self.product_variant_id}'
