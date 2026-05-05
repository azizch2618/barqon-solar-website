from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_companyprofile_contact_created_at_contact_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="ac",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="battery_preference",
            field=models.CharField(
                choices=[
                    ("lithium", "Lithium"),
                    ("lead_acid", "Lead Acid"),
                    ("either", "Either"),
                    ("no_battery", "No Battery"),
                ],
                default="either",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="city_area",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="contact",
            name="computers",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="desired_backup_hours",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name="contact",
            name="fans",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="fridge",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="heater",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="installation_address",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="iron",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="lead_status",
            field=models.CharField(
                choices=[
                    ("new", "New"),
                    ("contacted", "Contacted"),
                    ("quoted", "Quoted"),
                    ("closed", "Closed"),
                ],
                default="new",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="lights",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="load_details",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="monthly_bill",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="motors",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="other_load_watts",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contact",
            name="owner_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="preferred_contact_method",
            field=models.CharField(
                choices=[("call", "Call"), ("whatsapp", "WhatsApp"), ("email", "Email")],
                default="call",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="property_type",
            field=models.CharField(
                choices=[
                    ("home", "Home"),
                    ("shop", "Shop"),
                    ("hotel", "Hotel"),
                    ("restaurant", "Restaurant"),
                    ("office", "Office"),
                    ("factory", "Factory"),
                    ("other", "Other"),
                ],
                default="home",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="system_type_preference",
            field=models.CharField(
                choices=[
                    ("hybrid", "Hybrid"),
                    ("on_grid", "On Grid"),
                    ("off_grid", "Off Grid"),
                    ("not_sure", "Not Sure"),
                ],
                default="not_sure",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="wants_earth_bore",
            field=models.BooleanField(default=False),
        ),
    ]
