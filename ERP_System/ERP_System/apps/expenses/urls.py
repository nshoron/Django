from rest_framework.routers import DefaultRouter
from .views import ExpenseCategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register('categories', ExpenseCategoryViewSet)
router.register('expenses', ExpenseViewSet)

urlpatterns = router.urls
