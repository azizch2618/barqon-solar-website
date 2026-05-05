from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


User = get_user_model()


class BlogApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="strongpass123",
            is_admin=True,
            is_staff=True,
        )

    def test_public_blog_list_only_shows_published_posts(self):
        Post.objects.create(title="Published", content="Visible", is_published=True)
        Post.objects.create(title="Draft", content="Hidden", is_published=False)

        response = self.client.get(reverse("blog-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Published")

    def test_owner_can_create_blog_post(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            reverse("blog-list"),
            {
                "title": "Solar Benefits",
                "excerpt": "Quick overview",
                "content": "Solar reduces grid dependency.",
                "is_published": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.owner)

    def test_public_blog_page_loads(self):
        post = Post.objects.create(title="Solar Benefits", content="Useful content", is_published=True)

        response = self.client.get(reverse("blog-page"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, post.title)
