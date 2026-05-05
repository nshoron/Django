from rest_framework import viewsets


from .models import Product, ProductImage, ProductVariant
from .serializers import ProductImageSerializer, ProductSerializer, ProductVariantSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('brand', 'category')
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related('product')
    serializer_class = ProductImageSerializer


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.select_related('product', 'size', 'color')
    serializer_class = ProductVariantSerializer
