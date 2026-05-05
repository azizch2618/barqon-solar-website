from django.contrib import admin
from django.utils.html import format_html
from .models import Quotation


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        "quotation_number",
        "customer_name",
        "system_summary",
        "total_cost_display",
        "status_badge",
        "pdf_download",
        "created_at",
    )
    list_filter = ("status", "created_at", "inverter_type", "battery_type")
    search_fields = ("quotation_number", "customer_name", "customer_phone", "customer_email")
    readonly_fields = ("quotation_number", "subtotal", "total_cost", "created_at", "updated_at")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("lead", "prepared_by")

    
    fieldsets = (
        ("Client Information", {
            "fields": (("quotation_number", "status"), ("lead", "customer_user"), ("customer_name", "customer_phone", "customer_email"), "address")
        }),
        ("System Specifications", {
            "fields": (("system_size", "monthly_units"), ("panel_brand", "panel_wattage", "panel_count"), ("inverter_brand", "inverter_type", "inverter_size_kw"), ("battery_type", "battery_brand", "battery_size_kwh"))
        }),
        ("Financials", {
            "fields": (("subtotal", "discount", "tax_percentage", "tax_amount"), "total_cost", ("monthly_savings", "roi_years"))
        }),
        ("Timeline & Terms", {
            "fields": ("valid_until", "delivery_timeline", "payment_terms", "warranty_terms", "notes")
        }),
    )

    def system_summary(self, obj):
        return format_html(
            '<b>{}kW</b><br/><small>{} panels • {}</small>',
            obj.system_size, obj.panel_count, obj.inverter or "Hybrid"
        )
    system_summary.short_description = "System Config"

    def total_cost_display(self, obj):
        cost = f"Rs {obj.total_cost:,.0f}" if obj.total_cost else "Rs 0"
        return format_html('<span style="font-weight: bold; color: #10b981;">{}</span>', cost)
    total_cost_display.short_description = "Total Cost"


    def status_badge(self, obj):
        colors = {
            'draft': '#64748b',
            'sent': '#3b82f6',
            'approved': '#10b981',
            'rejected': '#ef4444',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def pdf_download(self, obj):
        url = f"/api/quotations/{obj.id}/pdf/"
        return format_html(
            '<a href="{}" target="_blank" style="background-color: #3b82f6; color: white; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 11px;"><i class="fas fa-file-pdf"></i> PDF</a>',
            url
        )
    pdf_download.short_description = "Actions"

