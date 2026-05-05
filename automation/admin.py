from django.contrib import admin
from .models import Lead, SolarCalculation, Proposal

class SolarCalculationInline(admin.StackedInline):
    model = SolarCalculation
    extra = 0

class ProposalInline(admin.TabularInline):
    model = Proposal
    extra = 0
    readonly_fields = ('created_at', 'pdf_file')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'monthly_units', 'system_size', 'estimated_cost', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('name', 'phone', 'city')
    inlines = [SolarCalculationInline, ProposalInline]

@admin.register(SolarCalculation)
class SolarCalculationAdmin(admin.ModelAdmin):
    list_display = ('lead', 'system_size_kw', 'monthly_savings', 'payback_years', 'total_cost', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('lead__name', 'lead__phone')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('lead', 'version', 'status', 'pdf_file', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('lead__name', 'lead__phone')
