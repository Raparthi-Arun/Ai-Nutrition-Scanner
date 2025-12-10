from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutritionScanViewSet, DailyNutritionLogViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'scans', NutritionScanViewSet, basename='nutrition-scan')
router.register(r'daily-logs', DailyNutritionLogViewSet, basename='daily-log')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
