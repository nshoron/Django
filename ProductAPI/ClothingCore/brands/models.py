from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
