from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_contact_linked_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="wapda_bill",
            field=models.FileField(blank=True, null=True, upload_to="bills/"),
        ),
    ]
