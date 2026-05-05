from datetime import timedelta

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def populate_quotation_numbers(apps, schema_editor):
    Quotation = apps.get_model("quotations", "Quotation")
    year = timezone.now().year

    for index, quotation in enumerate(Quotation.objects.all().order_by("id"), start=1):
        quotation.quotation_number = f"BARQON-{year}-{index:04d}"
        if not quotation.valid_until:
            quotation.valid_until = timezone.localdate() + timedelta(days=15)
        quotation.save(update_fields=["quotation_number", "valid_until"])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quotations", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quotation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="quotation",
            name="battery_size_kwh",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="quotation",
            name="customer_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="quotation",
            name="customer_phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="quotation",
            name="discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="inverter_size_kw",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="quotation",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="quotation",
            name="panel_capacity_kw",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="quotation",
            name="prepared_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="quotations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="quotation",
            name="project_title",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="quotation",
            name="quotation_number",
            field=models.CharField(blank=True, default="", max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="quotation",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("sent", "Sent"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="quotation",
            name="subtotal",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="tax_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="quotation",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="quotation",
            name="valid_until",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="quotation",
            name="total_cost",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.RunPython(populate_quotation_numbers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="quotation",
            name="quotation_number",
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
