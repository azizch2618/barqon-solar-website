from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


def populate_post_slugs(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    for post in Post.objects.all().order_by("id"):
        base_slug = slugify(post.title) or "barqon-blog-post"
        slug = base_slug
        counter = 1
        while Post.objects.exclude(pk=post.pk).filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"
        post.slug = slug
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="excerpt",
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name="post",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=220),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.RunPython(populate_post_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=220, unique=True),
        ),
    ]
