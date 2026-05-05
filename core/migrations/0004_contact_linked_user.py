from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_contact_city_area_contact_computers_contact_desired_backup_hours_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="linked_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="customer_leads",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
