from django.db import models


class ProductTag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class ProductTagMap(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='tag_links'
    )
    tag = models.ForeignKey(
        ProductTag,
        on_delete=models.CASCADE,
        related_name='product_links'
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'tag'],
                name='unique_product_tag'
            )
        ]

    def __str__(self):
        return f'{self.product_id} - {self.tag_id}'