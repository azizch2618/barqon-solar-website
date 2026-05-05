from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotations", "0003_quotation_battery_backup_hours_quotation_battery_brand_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quotation",
            name="system_size",
            field=models.FloatField(help_text="Recommended or proposed solar system size in kW."),
        ),
        migrations.AlterField(
            model_name="quotation",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
