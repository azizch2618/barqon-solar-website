from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from core.models import StaffProfile


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Details'
    fk_name = 'user'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (StaffProfileInline,)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_admin",)}),)
    list_display = ("username", "email", "is_staff", "is_admin", "is_superuser")

