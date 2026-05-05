from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
