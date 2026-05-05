from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuotationViewSet, generate_pdf, render_quotation_view

router = DefaultRouter()
router.register("", QuotationViewSet, basename="quotation")

urlpatterns = router.urls + [
    path("<int:id>/pdf/", generate_pdf, name="quotation-pdf"),
    path("<int:id>/view/", render_quotation_view, name="quotation-view"),
]
