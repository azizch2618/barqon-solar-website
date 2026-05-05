from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import CompanyProfile, Contact, Project, StaffProfile
from quotations.models import Quotation


class QuotationInline(admin.TabularInline):
    model = Quotation
    extra = 0
    fields = ("quotation_number", "system_size", "total_cost", "status", "created_at")
    readonly_fields = fields


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    fields = ("title", "status", "assigned_engineer", "installation_date")


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email", "updated_at")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "city_area", "lead_status", "status_badge", "assigned_to", "is_resolved", "created_at")
    list_filter = ("property_type", "lead_status", "is_resolved", "created_at", "assigned_to")
    search_fields = ("name", "phone", "email", "city_area")
    list_editable = ("lead_status", "assigned_to")
    inlines = [QuotationInline, ProjectInline]

    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("assigned_to")

    
    def status_badge(self, obj):
        colors = {
            'new': '#3b82f6',         # Blue
            'contacted': '#f59e0b',   # Yellow/Orange
            'quoted': '#8b5cf6', # Purple
            'won': '#10b981',         # Green
            'lost': '#ef4444',        # Red
            'closed': '#64748b',      # Slate
        }
        color = colors.get(obj.lead_status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_lead_status_display()
        )
    status_badge.short_description = "Status"

    def save_model(self, request, obj, form, change):
        # Automation: Auto-create project if lead status becomes 'won' and no project exists
        if obj.lead_status == 'won' and not obj.projects.exists():
            Project.objects.create(
                lead=obj,
                title=f"Project for {obj.name}",
                location=obj.city_area,
                status='pending'
            )
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "lead_link", "status", "status_badge", "assigned_engineer", "installation_date")
    list_filter = ("status", "installation_date", "assigned_engineer")
    search_fields = ("title", "lead__name", "location")
    list_editable = ("status", "assigned_engineer", "installation_date")


    def get_queryset(self, request):
        return super().get_queryset(request).select_related("lead", "assigned_engineer")


    def lead_link(self, obj):
        if obj.lead:
            url = reverse("admin:core_contact_change", args=[obj.lead.id])
            return format_html('<a href="{}">{}</a>', url, obj.lead.name)
        return "—"
    lead_link.short_description = "Lead"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'in_progress': '#3b82f6',
            'completed': '#10b981',
            'on_hold': '#ef4444',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "phone", "salary_info", "commission_per_lead", "is_active")
    list_filter = ("role", "is_active", "salary_type")
    search_fields = ("name", "email", "phone")
    
    def salary_info(self, obj):
        if obj.salary_type == 'monthly':
            return f"Rs {obj.monthly_salary}/mo"
        return f"Rs {obj.daily_wage}/day"
    salary_info.short_description = "Salary/Wage"

