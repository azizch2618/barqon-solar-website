from django.db import models
from django.utils import timezone
import os

class Lead(models.Model):
    LEAD_TYPE_QUICK = 'quick'
    LEAD_TYPE_DETAILED = 'detailed'
    
    LEAD_TYPE_CHOICES = [
        (LEAD_TYPE_QUICK, 'Quick Inquiry'),
        (LEAD_TYPE_DETAILED, 'Detailed Engineering'),
    ]
    
    LEAD_STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted'),
        ('survey_scheduled', 'Survey Scheduled'),
        ('closed', 'Closed (Won)'),
        ('lost', 'Lost'),
    ]
    
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    monthly_units = models.IntegerField(default=0)
    system_size = models.FloatField(null=True, blank=True)
    estimated_cost = models.FloatField(null=True, blank=True)
    appliance_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class SolarCalculation(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='calculation')
    system_size_kw = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_units = models.PositiveIntegerField()
    monthly_savings = models.DecimalField(max_digits=15, decimal_places=2)
    annual_savings = models.DecimalField(max_digits=15, decimal_places=2)
    payback_years = models.DecimalField(max_digits=5, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    panel_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calc for {self.lead.name} - {self.system_size_kw}kW"

class Proposal(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_FINAL = 'final'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_FINAL, 'Final'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='proposals')
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    pdf_file = models.FileField(upload_to='proposals/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal V{self.version} - {self.lead.name}"
