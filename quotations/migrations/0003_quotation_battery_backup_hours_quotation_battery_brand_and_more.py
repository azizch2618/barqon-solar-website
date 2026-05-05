from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotations", "0002_alter_quotation_options_quotation_battery_size_kwh_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quotation",
            name="battery_backup_hours",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name="quotation",
            name="battery_brand",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="quotation",
            name="battery_type",
            field=models.CharField(
                choices=[("lithium", "Lithium"), ("lead_acid", "Lead Acid")],
                default="lithium",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="quotation",
            name="client_request_summary",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="quotation",
            name="earth_bore_included",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="quotation",
            name="earth_bore_rate",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="quotation",
            name="inverter_brand",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="quotation",
            name="panel_brand",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="quotation",
            name="panel_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="quotation",
            name="panel_wattage",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="quotation",
            name="recommended_brands",
            field=models.TextField(blank=True),
        ),
    ]
