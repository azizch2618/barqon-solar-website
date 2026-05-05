from django.urls import path

from .views import (
    blog_detail_page,
    blog_list_page,
    customer_dashboard,
    customer_logout_page,
    quotation_pdf_download_page,
    quotation_view_page,
    admin_dashboard,
    unified_login_view,
    unified_register_view,
    projects_gallery_view,
    reviews_gallery_view,
    about_us_view,
    careers_view,
    job_apply_view,
    general_apply_view,
)
from .payroll_views import generate_payroll_slip_pdf

urlpatterns = [
    path("login/", unified_login_view, name="login"),
    path("register/", unified_register_view, name="register"),
    path("portal/logout/", customer_logout_page, name="customer-logout"),
    path("portal/dashboard/", customer_dashboard, name="customer-dashboard"),
    path("portal/quotations/<int:id>/pdf/", quotation_pdf_download_page, name="customer-quotation-pdf"),
    path("portal/quotations/<int:id>/view/", quotation_view_page, name="customer-quotation-view"),

    path("admin-dashboard/payroll/<int:payroll_id>/pdf/", generate_payroll_slip_pdf, name="payroll-slip-pdf"),
    path("gallery/", projects_gallery_view, name="projects-gallery"),
    path("reviews/", reviews_gallery_view, name="reviews-gallery"),
    path("about/", about_us_view, name="about-page"),
    path("careers/", careers_view, name="careers-page"),
    path("careers/apply/<int:position_id>/", job_apply_view, name="job-apply"),
    path("careers/general-apply/", general_apply_view, name="general-apply"),
    path("insights/", blog_list_page, name="blog-page"),
    path("insights/<slug:slug>/", blog_detail_page, name="blog-detail-page"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/<path:path>/", admin_dashboard, name="react-app-catchall"),
    path("admin-login/", admin_dashboard, name="react-app-login"),
]
