from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_post_options_post_author_post_excerpt_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
