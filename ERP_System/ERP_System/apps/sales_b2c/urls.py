from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("customers", CustomerViewSet)
router.register("sales", SaleViewSet)
router.register("sale-items", SaleItemViewSet)
router.register("bills", BillViewSet)
router.register("returns", ReturnViewSet)
router.register("return-items", ReturnItemViewSet)

urlpatterns = router.urls