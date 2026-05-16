from rest_framework.routers import DefaultRouter
from .views import LedgerAccountViewSet, AccountingTransactionViewSet

router = DefaultRouter()
router.register('ledgers', LedgerAccountViewSet)
router.register('transactions', AccountingTransactionViewSet)

urlpatterns = router.urls
