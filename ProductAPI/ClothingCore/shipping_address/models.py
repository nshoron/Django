from django.conf import settings
from django.db import models


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipping_addresses',
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    address_line = models.TextField()
    city = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=32)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.full_name}, {self.city}'
