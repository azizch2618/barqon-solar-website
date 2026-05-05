from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loadcalculation",
            name="city_area",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="loadcalculation",
            name="computers",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="loadcalculation",
            name="heater",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="loadcalculation",
            name="iron",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="loadcalculation",
            name="motors",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="loadcalculation",
            name="property_type",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
