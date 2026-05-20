from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_home,
    dashboard_summary,
    CompanyProfileViewSet,
    ContactViewSet,
    ProjectViewSet,
    StaffProfileViewSet,
    PayrollViewSet,
    SiteReviewViewSet,
    InstallationProjectViewSet,
    ProjectFinancialsViewSet,
    JobPositionViewSet,
    JobApplicationViewSet,
    ProjectPaymentViewSet,
    InventoryItemViewSet,
)

router = DefaultRouter()
router.register(r'company-profile', CompanyProfileViewSet, basename='company-profile')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'staff', StaffProfileViewSet, basename='staff')
router.register(r'payroll', PayrollViewSet, basename='payroll')
router.register(r'site-reviews', SiteReviewViewSet, basename='site-review')
router.register(r'installations', InstallationProjectViewSet, basename='installation')
router.register(r'project-financials', ProjectFinancialsViewSet, basename='project-financials')
router.register(r'job-positions', JobPositionViewSet, basename='job-position')
router.register(r'job-applications', JobApplicationViewSet, basename='job-application')
router.register(r'project-payments', ProjectPaymentViewSet, basename='project-payment')
router.register(r'inventory', InventoryItemViewSet, basename='inventory')


urlpatterns = [
    path("contact/submit/", ContactViewSet.as_view({"post": "create"}), name="contact-list-create"),
    path("", include(router.urls)),
    path("api-root/", api_home, name="api-home"),
    path("dashboard-summary/", dashboard_summary, name="dashboard-summary"),
    path("dashboard/", dashboard_summary, name="dashboard"),
]
