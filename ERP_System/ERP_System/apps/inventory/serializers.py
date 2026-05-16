from rest_framework import serializers
from .models import *


class InventorySerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField()

    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryLogSerializer(serializers.ModelSerializer):
    inventory = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = InventoryLog
        fields = "__all__"