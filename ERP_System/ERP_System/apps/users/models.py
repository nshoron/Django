from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("warehouse_staff", "Warehouse Staff"),
        ("warehouse", "Warehouse"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="warehouse_staff"
    )

    REQUIRED_FIELDS = []   
