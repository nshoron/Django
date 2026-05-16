from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *
from core.permissions import IsAdminManagerOrReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']


class SizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['name', 'color_code']
    ordering_fields = ['name']


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category", "brand").prefetch_related("variants")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['name', 'brand__name', 'category__name']
    ordering_fields = ['name', 'category', 'brand']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        brand_id = self.request.query_params.get("brand")
        size_id = self.request.query_params.get("size")
        color_id = self.request.query_params.get("color")
        name = self.request.query_params.get("name")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if size_id:
            queryset = queryset.filter(variants__size_id=size_id)
        if color_id:
            queryset = queryset.filter(variants__color_id=color_id)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get products by category"""
        category_id = request.query_params.get('category_id')
        if category_id:
            products = Product.objects.filter(category_id=category_id)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'category_id is required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_brand(self, request):
        """Get products by brand"""
        brand_id = request.query_params.get('brand_id')
        if brand_id:
            products = Product.objects.filter(brand_id=brand_id)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'brand_id is required'}, status=400)


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.select_related("product", "size", "color")
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ['product_code', 'product__name']
    ordering_fields = ['product_code']

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get("product")
        category_id = self.request.query_params.get("category")
        brand_id = self.request.query_params.get("brand")
        size_id = self.request.query_params.get("size")
        color_id = self.request.query_params.get("color")
        product_code = self.request.query_params.get("product_code")

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)
        if brand_id:
            queryset = queryset.filter(product__brand_id=brand_id)
        if size_id:
            queryset = queryset.filter(size_id=size_id)
        if color_id:
            queryset = queryset.filter(color_id=color_id)
        if product_code:
            queryset = queryset.filter(product_code__iexact=product_code)

        return queryset
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """Get variants by product"""
        product_id = request.query_params.get('product_id')
        if product_id:
            variants = ProductVariant.objects.filter(product_id=product_id)
            serializer = self.get_serializer(variants, many=True)
            return Response(serializer.data)
        return Response({'error': 'product_id is required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_product_code(self, request):
        """Get variant by product code"""
        product_code = request.query_params.get('product_code')
        if product_code:
            try:
                variant = ProductVariant.objects.get(product_code=product_code)
                serializer = self.get_serializer(variant)
                return Response(serializer.data)
            except ProductVariant.DoesNotExist:
                return Response({'error': 'Product variant not found'}, status=404)
        return Response({'error': 'product_code is required'}, status=400)

