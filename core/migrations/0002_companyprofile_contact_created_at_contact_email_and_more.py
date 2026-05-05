from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(default="BARQON Solar Solutions", max_length=200)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("whatsapp", models.CharField(blank=True, max_length=30)),
                ("website", models.URLField(blank=True)),
                ("address", models.TextField(blank=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="company/")),
                (
                    "footer_note",
                    models.TextField(blank=True, help_text="Footer text for quotations and public profile."),
                ),
                ("bank_details", models.TextField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Company Profile",
                "verbose_name_plural": "Company Profile",
            },
        ),
        migrations.AddField(
            model_name="contact",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="contact",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="contact",
            name="is_resolved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contact",
            name="subject",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterModelOptions(
            name="contact",
            options={"ordering": ["-created_at"]},
        ),
    ]
