from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_contact_is_viewed"),
    ]

    operations = [
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("sku", models.CharField(blank=True, db_index=True, max_length=64)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("panels", "Solar Panels"),
                            ("inverters", "Inverters"),
                            ("batteries", "Batteries"),
                            ("mounting", "Mounting"),
                            ("electrical", "Electrical"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=32,
                    ),
                ),
                ("quantity_on_hand", models.PositiveIntegerField(default=0)),
                ("reorder_level", models.PositiveIntegerField(default=5)),
                ("unit_cost", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("supplier", models.CharField(blank=True, max_length=200)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "inventory item",
                "verbose_name_plural": "inventory items",
                "ordering": ["name"],
            },
        ),
    ]
