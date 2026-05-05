from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=220)
    excerpt = models.CharField(max_length=300, blank=True)
    content = RichTextField()
    image = models.ImageField(upload_to="insights/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="External image URL (e.g. Unsplash)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_published = models.BooleanField(default=False) # Keep for backward compatibility
    
    # Extra Features
    author_name = models.CharField(max_length=100, default="BARQON Team")
    read_time = models.CharField(max_length=20, default="3 min read")
    category = models.CharField(max_length=100, default="Solar Solutions")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")
    
    # SEO Fields
    meta_title = models.CharField(max_length=150, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to="insights/seo/", blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Sync is_published with status
        if self.status == 'published':
            self.is_published = True
        else:
            self.is_published = False

        if not self.excerpt and self.content:
            plain_text = strip_tags(self.content).strip()
            self.excerpt = plain_text[:297] + "..." if len(plain_text) > 300 else plain_text

        if not self.meta_title:
            self.meta_title = self.title

        desired_base_slug = slugify(self.title) or "barqon-blog-post"
        if not self.slug or slugify(self.title) not in self.slug:
            slug = desired_base_slug
            counter = 1
            while Post.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                counter += 1
                slug = f"{desired_base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="insights/gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Image for {self.post.title}"
