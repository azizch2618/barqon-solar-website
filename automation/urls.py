from django.urls import path
from .views import submit_lead_view, admin_leads

urlpatterns = [
    path('submit-lead/', submit_lead_view, name='submit-lead'),
    path('admin-leads/', admin_leads, name='admin-leads'),
]
