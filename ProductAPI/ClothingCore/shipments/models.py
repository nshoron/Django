from django.conf import settings
from django.db import models


class ShippingAddress(models.Model):
    order = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipments',
    )
    tracking_number=models.CharField(max_length=200)
    status=models.CharField(max_length=200)


    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.tracking_number}, {self.status}'
