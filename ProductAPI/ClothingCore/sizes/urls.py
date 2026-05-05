from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SizeViewSet

router = DefaultRouter()
router.register('sizes', SizeViewSet, basename='size')

urlpatterns = [path('', include(router.urls))]
