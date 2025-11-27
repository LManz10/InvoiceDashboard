from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AnalyzeView, ReportViewSet, ValidationRunViewSet, FilterViewSet

router = DefaultRouter()
#router.register(r"reports", ReportViewSet, basename="report")
router.register(r"runs", ReportViewSet, basename="report")
router.register(r"filtered-runs", FilterViewSet, basename="filter-view")

urlpatterns = router.urls + [
    path("analyze/", AnalyzeView.as_view(), name="analyzeOneReport"),
]
