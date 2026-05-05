from django.conf import settings
from django.db import models


class LoadCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="load_calculations",
    )
    customer_name = models.CharField(max_length=120, blank=True)
    property_type = models.CharField(max_length=30, blank=True)
    city_area = models.CharField(max_length=150, blank=True)
    fans = models.PositiveIntegerField(default=0)
    lights = models.PositiveIntegerField(default=0)
    ac = models.PositiveIntegerField(default=0)
    fridge = models.PositiveIntegerField(default=0)
    heater = models.PositiveIntegerField(default=0)
    iron = models.PositiveIntegerField(default=0)
    computers = models.PositiveIntegerField(default=0)
    motors = models.PositiveIntegerField(default=0)
    other_load_watts = models.PositiveIntegerField(default=0)
    average_sun_hours = models.DecimalField(max_digits=4, decimal_places=2, default=5)
    backup_hours = models.DecimalField(max_digits=4, decimal_places=2, default=5)
    battery_voltage = models.PositiveIntegerField(default=12)
    total_load_watts = models.DecimalField(max_digits=12, decimal_places=2)
    diversified_load_watts = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solar_required_kw = models.DecimalField(max_digits=10, decimal_places=2)
    battery_required_ah = models.DecimalField(max_digits=12, decimal_places=2)
    battery_required_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    inverter_required_kw = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name or 'Unnamed calculation'} - {self.total_load_watts}W"
