from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import Contact


class Quotation(models.Model):
    BATTERY_LITHIUM = "lithium"
    BATTERY_LEAD_ACID = "lead_acid"

    BATTERY_TYPE_CHOICES = [
        (BATTERY_LITHIUM, "Lithium"),
        (BATTERY_LEAD_ACID, "Lead Acid"),
    ]

    STATUS_DRAFT = "draft"
    STATUS_SENT = "sent"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    quotation_number = models.CharField(max_length=30, unique=True, blank=True)
    lead = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotations",
    )
    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_quotations",
    )
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    project_title = models.CharField(max_length=200, blank=True)
    system_size = models.FloatField(help_text="Recommended or proposed solar system size in kW.")
    monthly_units = models.PositiveIntegerField(default=0)
    peak_load_kw = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    
    panel_capacity_kw = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    panel_wattage = models.PositiveIntegerField(default=0)
    panel_count = models.PositiveIntegerField(default=0)
    panel_brand = models.CharField(max_length=120, blank=True)
    panel_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    inverter = models.CharField(max_length=100)
    inverter_brand = models.CharField(max_length=120, blank=True)
    inverter_type = models.CharField(max_length=50, blank=True, help_text="e.g., Hybrid, On-Grid")
    inverter_size_kw = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    inverter_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    battery = models.CharField(max_length=100, blank=True)
    battery_type = models.CharField(
        max_length=20,
        choices=BATTERY_TYPE_CHOICES,
        default=BATTERY_LITHIUM,
    )
    battery_brand = models.CharField(max_length=120, blank=True)
    battery_size_kwh = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    battery_backup_hours = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    battery_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    structure_type = models.CharField(max_length=50, blank=True, help_text="e.g., L1, L2, L3, Custom")
    structure_material = models.CharField(max_length=100, blank=True)
    mounting_structure_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    dc_wire_length_m = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    dc_wire_size_mm = models.CharField(max_length=50, blank=True)
    dc_wire_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    ac_wire_length_m = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    ac_wire_size_mm = models.CharField(max_length=50, blank=True)
    ac_wire_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    breaker_type = models.CharField(max_length=50, blank=True, help_text="e.g., MCB, MCCB")
    breaker_rating = models.CharField(max_length=50, blank=True)
    breaker_count = models.PositiveIntegerField(default=0)
    breaker_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    spd_type = models.CharField(max_length=50, blank=True, help_text="e.g., Type 1, Type 2")
    spd_count = models.PositiveIntegerField(default=0)
    spd_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    earth_bore_qty = models.PositiveIntegerField(default=0)
    earth_bore_included = models.BooleanField(default=False)
    earth_bore_rate = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    
    installation_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    net_metering_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    transport_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    miscellaneous_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"), help_text="Tax percentage to apply to subtotal")
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    total_load_watts = models.PositiveIntegerField(default=0)
    monthly_savings = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    roi_years = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    recommended_brands = models.TextField(blank=True)
    client_request_summary = models.TextField(blank=True)
    load_details = models.JSONField(default=dict, blank=True, help_text="Appliance load details JSON")
    notes = models.TextField(blank=True)
    payment_terms = models.TextField(blank=True)
    warranty_terms = models.TextField(blank=True)
    delivery_timeline = models.CharField(max_length=200, blank=True)
    # Electrical & Protection Components
    db_size = models.CharField(max_length=50, blank=True, help_text="e.g., 6 Way, 12 Way")
    db_rate = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    db_qty = models.PositiveIntegerField(default=1)
    wiring_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    earthing_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    # Protection Devices (Legacy - keep for compatibility)
    mcb_qty = models.PositiveIntegerField(default=0)
    mcb_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    mccb_qty = models.PositiveIntegerField(default=0)
    mccb_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    isolator_qty = models.PositiveIntegerField(default=0)
    isolator_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    # New Structured Breakers
    # Format: [{"type": "MCB", "amp": "32A", "qty": 2, "rate": 1500, "total": 3000}, ...]
    breaker_items = models.JSONField(default=list, blank=True)
    
    # Miscellaneous Items (Dynamic Rows)
    # Format: [{"name": "Cable Ties", "qty": 10, "price": 50, "total": 500}, ...]
    miscellaneous_items = models.JSONField(default=list, blank=True)
    
    # Tax System (Enhanced)
    TAX_TYPE_PERCENTAGE = "percentage"
    TAX_TYPE_FIXED = "fixed"
    TAX_TYPE_CHOICES = [
        (TAX_TYPE_PERCENTAGE, "Percentage (%)"),
        (TAX_TYPE_FIXED, "Fixed (PKR)"),
    ]
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES, default=TAX_TYPE_PERCENTAGE)
    
    # Page Selection System
    # Format: ["summary", "terms", "load", "technical", "signature"]
    include_pages = models.JSONField(default=list, blank=True)
    
    # General Fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    valid_until = models.DateField(blank=True, null=True)
    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Versioning & Negotiation System
    parent_quotation = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='revisions',
        help_text="The original quotation this version was revised from."
    )
    version_number = models.PositiveIntegerField(default=1)
    change_notes = models.TextField(blank=True, help_text="Internal notes about what changed in this version.")
    negotiation_notes = models.TextField(blank=True, help_text="Notes specifically related to client negotiations.")
    is_negotiation_mode = models.BooleanField(default=False, help_text="If true, allows manual rate and discount overrides.")
    is_final = models.BooleanField(default=False, help_text="Locks the quotation from further edits.")

    class Meta:
        ordering = ["-created_at"]

    @staticmethod
    def _to_decimal(value):
        return Decimal(str(value or "0.00"))

    def component_lines(self):
        lines = [
            {
                "label": f"Solar Panels ({self.panel_brand or 'Standard'})",
                "specs": f"{self.panel_wattage}W",
                "quantity": self.panel_count,
                "unit": self.panel_unit_price,
                "total": self._to_decimal(self.panel_count) * self.panel_unit_price,
            },
            {
                "label": f"Inverter ({self.inverter_brand or 'Standard'})",
                "specs": f"{float(self.inverter_size_kw):.2f} kW {self.inverter_type}",
                "quantity": 1 if self.inverter_unit_price else 0,
                "unit": self.inverter_unit_price,
                "total": self.inverter_unit_price,
            },
            {
                "label": f"Battery Bank ({self.battery_brand or 'Standard'})",
                "specs": f"{self.battery_size_kwh} kWh {self.get_battery_type_display()} ({self.battery_backup_hours}h backup)",
                "quantity": 1 if self.battery_unit_price else 0,
                "unit": self.battery_unit_price,
                "total": self.battery_unit_price,
            },
            {
                "label": f"Mounting Structure ({self.structure_type or 'Standard'})",
                "specs": self.structure_material or "Galvanized Iron",
                "quantity": 1 if self.mounting_structure_cost else 0,
                "unit": self.mounting_structure_cost,
                "total": self.mounting_structure_cost,
            },
            # DC Cable
            {
                "label": f"DC Cable ({self.dc_wire_size_mm or '4mm/6mm'})",
                "specs": f"Rate: PKR {self.dc_wire_unit_price}/meter (Final length confirmed on site)",
                "quantity": "As req.",
                "unit": self.dc_wire_unit_price,
                "total": "Site Dependent",
            },
            # AC Cable
            {
                "label": f"AC Cable ({self.ac_wire_size_mm or '10mm/16mm'})",
                "specs": f"Rate: PKR {self.ac_wire_unit_price}/meter (Final length confirmed on site)",
                "quantity": "As req.",
                "unit": self.ac_wire_unit_price,
                "total": "Site Dependent",
            },
            # Distribution Board
            {
                "label": f"Distribution Board ({self.db_size or 'Standard'})",
                "specs": "Complete with internal wiring",
                "quantity": self.db_qty,
                "unit": self.db_rate,
                "total": self._to_decimal(self.db_qty) * self.db_rate,
            },
            # Earthing
            {
                "label": "Earthing System (Bores)",
                "specs": f"{self.earth_bore_qty} Bores",
                "quantity": self.earth_bore_qty,
                "unit": self.earth_bore_rate,
                "total": self._to_decimal(self.earth_bore_qty) * self.earth_bore_rate,
            },
        ]
        
        # Add Structured Breakers
        for breaker in self.breaker_items:
            qty = self._to_decimal(breaker.get("qty", 0))
            rate = self._to_decimal(breaker.get("rate", 0))
            lines.append({
                "label": f"{breaker.get('type', 'Breaker')} ({breaker.get('amp', 'N/A')})",
                "specs": "Protection Device",
                "quantity": qty,
                "unit": rate,
                "total": qty * rate,
            })
            
        # Installation & Services
        lines.extend([
            {
                "label": "Installation and Commissioning",
                "specs": "Turnkey service",
                "quantity": 1 if self.installation_cost else 0,
                "unit": self.installation_cost,
                "total": self.installation_cost,
            },
            {
                "label": "Net Metering Support",
                "specs": "Documentation and processing",
                "quantity": 1 if self.net_metering_cost else 0,
                "unit": self.net_metering_cost,
                "total": self.net_metering_cost,
            },
            {
                "label": "Transport and Logistics",
                "specs": "Delivery to site",
                "quantity": 1 if self.transport_cost else 0,
                "unit": self.transport_cost,
                "total": self.transport_cost,
            },
        ])
        
        # Add Miscellaneous Items
        for item in self.miscellaneous_items:
            qty = self._to_decimal(item.get("qty", 1))
            rate = self._to_decimal(item.get("price", 0))
            lines.append({
                "label": item.get("name", "Misc Item"),
                "specs": item.get("description", ""),
                "quantity": qty,
                "unit": rate,
                "total": qty * rate,
            })
            
        return [line for line in lines if line.get("total")]

    def itemized_subtotal(self):
        return sum((line["total"] for line in self.component_lines() if isinstance(line["total"], (int, float, Decimal))), Decimal("0.00"))

    def save(self, *args, **kwargs):
        # 1. Handle Versioning logic for NEW revisions
        if self.parent_quotation and not self.pk:
            # Find the root parent to maintain a consistent base number
            root = self.parent_quotation
            while root.parent_quotation:
                root = root.parent_quotation
            
            # Use the base number from root (strip any existing -V parts if any, though root shouldn't have them)
            base_number = root.quotation_number
            if "-V" in base_number:
                base_number = base_number.split("-V")[0]
            
            # Find the highest version number among all revisions of this root
            # We look for all quotes starting with base_number + "-V"
            latest_rev = Quotation.objects.filter(
                quotation_number__startswith=f"{base_number}-V"
            ).order_by('-version_number').first()
            
            if latest_rev:
                self.version_number = latest_rev.version_number + 1
            else:
                # If this is the first revision of a base quote
                self.version_number = max(root.version_number, 1) + 1
            
            self.quotation_number = f"{base_number}-V{self.version_number}"

        # 2. Generate Base Number if not set and NOT a revision
        if not self.quotation_number:
            year = timezone.now().year
            prefix = f"BARQON-{year}-"
            
            # Find the highest BASE quotation number (exactly matching the prefix + 4 digits)
            # This avoids picking up revisions like -V2 which would break the integer split
            last_base_quote = (
                Quotation.objects.filter(quotation_number__regex=rf"^{prefix}\d{{4}}$")
                .order_by("-quotation_number")
                .first()
            )
            
            next_id = 1
            if last_base_quote:
                try:
                    last_num_str = last_base_quote.quotation_number.split("-")[-1]
                    next_id = int(last_num_str) + 1
                except (ValueError, TypeError, IndexError):
                    # Fallback to count if split fails
                    next_id = Quotation.objects.filter(parent_quotation__isnull=True).count() + 1
            
            self.quotation_number = f"{prefix}{next_id:04d}"

        if not self.valid_until:
            self.valid_until = timezone.localdate() + timedelta(days=15)

        # Dynamic Subtotal Calculation
        self.subtotal = self.itemized_subtotal()
        
        # Enhanced Tax Calculation
        if self.tax_type == self.TAX_TYPE_PERCENTAGE:
            self.tax_amount = (self.subtotal - self.discount) * (self.tax_percentage / 100)
        else:
            # If tax_type is fixed, tax_amount is likely set manually via API, 
            # but we keep it flexible.
            pass

        self.total_cost = max(self.subtotal - self.discount + self.tax_amount, Decimal("0.00"))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quotation_number} - {self.customer_name}"
