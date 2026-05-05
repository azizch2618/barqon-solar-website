from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AccountsApiTests(APITestCase):
    def test_registration_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newowner",
                "password": "verystrong123",
                "email": "owner@example.com",
                "first_name": "Barqon",
                "last_name": "Owner",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newowner").exists())
