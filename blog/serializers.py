from rest_framework import serializers

from .models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]


class PostSerializer(serializers.ModelSerializer):
    photos = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "image",
            "status",
            "is_published",
            "author_name",
            "read_time",
            "category",
            "tags",
            "meta_title",
            "meta_description",
            "og_image",
            "author",
            "photos",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "author", "created_at", "updated_at"]
