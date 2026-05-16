from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentTransactionViewSet

router = DefaultRouter()
router.register('payments', PaymentViewSet)
router.register('payment-transactions', PaymentTransactionViewSet)

urlpatterns = router.urls
