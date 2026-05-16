from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("suppliers", SupplierViewSet)
router.register("purchases", PurchaseViewSet)
router.register("purchase-items", PurchaseItemViewSet)
router.register("purchase-returns", PurchaseReturnViewSet)
router.register("purchase-return-items", PurchaseReturnItemViewSet)

urlpatterns = router.urls