from decimal import Decimal

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_contact_linked_user"),
        ("quotations", "0004_alter_quotation_system_size_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="quotation",
            name="ac_wire_length_m",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10),
        ),
        migrations.AddField(
            model_name="quotation",
            name="ac_wire_size_mm",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="quotation",
            name="ac_wire_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="battery_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="breaker_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="quotation",
            name="breaker_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="customer_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="customer_quotations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="quotation",
            name="dc_wire_length_m",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10),
        ),
        migrations.AddField(
            model_name="quotation",
            name="dc_wire_size_mm",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="quotation",
            name="dc_wire_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="delivery_timeline",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="quotation",
            name="installation_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="inverter_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="lead",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="quotations",
                to="core.contact",
            ),
        ),
        migrations.AddField(
            model_name="quotation",
            name="miscellaneous_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="mounting_structure_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="net_metering_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="panel_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="payment_terms",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="quotation",
            name="spd_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="quotation",
            name="spd_unit_price",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="transport_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="warranty_terms",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="quotation",
            name="total_cost",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12),
        ),
    ]
