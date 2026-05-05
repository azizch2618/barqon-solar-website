from django.urls import path

from .views import owner_profile, register, staff_list_create

urlpatterns = [
    path("register/", register, name="api-register"),
    path("me/", owner_profile, name="owner-profile"),
    path("staff/", staff_list_create, name="staff-list"),
]
