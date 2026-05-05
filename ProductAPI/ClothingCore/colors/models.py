import re

from django.core.validators import RegexValidator
from django.db import models

_hex_validator = RegexValidator(
    regex=re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'),
    message='Enter a valid hex color, e.g. #FF5733 or #FFF.',
)


class Color(models.Model):
    name = models.CharField(max_length=64)
    hex_code = models.CharField(max_length=7, validators=[_hex_validator])

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
