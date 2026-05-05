from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductImageViewSet, ProductVariantViewSet, ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('product-images', ProductImageViewSet, basename='product-image')
router.register('product-variants', ProductVariantViewSet, basename='product-variant')

urlpatterns = [path('', include(router.urls))]
