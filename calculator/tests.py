from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import LoadCalculation


User = get_user_model()


class CalculatorApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="strongpass123",
            is_admin=True,
            is_staff=True,
        )

    def test_public_calculator_returns_solar_recommendations(self):
        response = self.client.post(
            reverse("calculate-load"),
            {
                "fans": 4,
                "lights": 8,
                "ac": 1,
                "fridge": 1,
                "other_load_watts": 250,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("solar_required_kw", response.data)
        self.assertIn("recommended_battery_size_kwh", response.data)

    def test_owner_can_save_calculation_and_view_history(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            reverse("calculate-load"),
            {
                "customer_name": "Factory Roof",
                "fans": 10,
                "lights": 20,
                "ac": 2,
                "fridge": 1,
                "other_load_watts": 500,
                "save_result": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LoadCalculation.objects.count(), 1)

        history_response = self.client.get(reverse("calculation-history"))
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(history_response.data), 1)
