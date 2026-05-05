from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0002_loadcalculation_city_area_loadcalculation_computers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="loadcalculation",
            name="diversified_load_watts",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
