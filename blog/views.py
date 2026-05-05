from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.permissions import IsOwnerOrAdmin

from .models import Post, PostImage
from .serializers import PostSerializer, PostImageSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_authenticated and (
            self.request.user.is_staff
            or self.request.user.is_superuser
            or getattr(self.request.user, "is_admin", False)
        ):
            return queryset
        return queryset.filter(is_published=True)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Handle multiple photos
        photos = self.request.FILES.getlist('uploaded_photos')
        for photo in photos:
            PostImage.objects.create(post=post, image=photo)

    def perform_update(self, serializer):
        post = serializer.save()
        # Handle multiple photos (append new ones)
        photos = self.request.FILES.getlist('uploaded_photos')
        for photo in photos:
            PostImage.objects.create(post=post, image=photo)


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_permissions(self):
        return [IsOwnerOrAdmin()]
