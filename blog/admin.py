from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'author_name', 'created_at', 'is_published')
    list_filter = ('status', 'category', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'content', 'excerpt', 'image')
        }),
        ('Blog Meta', {
            'fields': ('author_name', 'read_time', 'tags', 'status')
        }),
        ('SEO Optimization', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'og_image')
        }),
        ('System Info', {
            'classes': ('collapse',),
            'fields': ('author', 'is_published')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    search_fields = ('title', 'content', 'excerpt', 'author_name')
