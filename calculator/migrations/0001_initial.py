from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LoadCalculation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(blank=True, max_length=120)),
                ("fans", models.PositiveIntegerField(default=0)),
                ("lights", models.PositiveIntegerField(default=0)),
                ("ac", models.PositiveIntegerField(default=0)),
                ("fridge", models.PositiveIntegerField(default=0)),
                ("other_load_watts", models.PositiveIntegerField(default=0)),
                ("average_sun_hours", models.DecimalField(decimal_places=2, default=5, max_digits=4)),
                ("backup_hours", models.DecimalField(decimal_places=2, default=5, max_digits=4)),
                ("battery_voltage", models.PositiveIntegerField(default=12)),
                ("total_load_watts", models.DecimalField(decimal_places=2, max_digits=12)),
                ("solar_required_kw", models.DecimalField(decimal_places=2, max_digits=10)),
                ("battery_required_ah", models.DecimalField(decimal_places=2, max_digits=12)),
                ("battery_required_kwh", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("inverter_required_kw", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name="load_calculations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
