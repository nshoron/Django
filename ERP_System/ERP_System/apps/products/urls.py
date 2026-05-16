from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("sizes", SizeViewSet)
router.register("colors", ColorViewSet)
router.register("products", ProductViewSet)
router.register("variants", ProductVariantViewSet)

urlpatterns = router.urls