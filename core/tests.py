from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact


User = get_user_model()


class CoreApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="strongpass123",
            is_admin=True,
            is_staff=True,
        )

    def test_public_contact_form_creates_lead(self):
        response = self.client.post(
            reverse("contact-list-create"),
            {
                "name": "Hamza",
                "email": "hamza@example.com",
                "phone": "03112223344",
                "subject": "Need a solar quote",
                "message": "Please contact me for a 5kW system.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)

    def test_root_homepage_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "BARQON")

    def test_public_homepage_requirement_form_creates_lead(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Ahsan",
                "phone": "03001112222",
                "email": "ahsan@example.com",
                "subject": "Need solar for home",
                "property_type": "home",
                "city_area": "Johar Town Lahore",
                "installation_address": "Street 1, Johar Town",
                "system_type_preference": "hybrid",
                "monthly_bill": "25000",
                "fans": 5,
                "lights": 10,
                "ac": 2,
                "fridge": 1,
                "heater": 1,
                "iron": 1,
                "computers": 1,
                "motors": 0,
                "other_load_watts": 300,
                "load_details": "Microwave and washing machine occasionally.",
                "desired_backup_hours": "4",
                "battery_preference": "lithium",
                "wants_earth_bore": "on",
                "preferred_contact_method": "whatsapp",
                "message": "Please suggest a good system.",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Contact.objects.count(), 1)

    def test_owner_can_open_dashboard_summary(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(reverse("dashboard-summary"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("quotation_count", response.data)

    def test_admin_dashboard_requires_login_and_loads(self):
        response = self.client.get(reverse("react-app-root"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.client.force_login(self.owner)
        response = self.client.get(reverse("react-app-root"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_login_redirects_to_unified_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "owner",
                "password": "strongpass123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("react-app-root"))

    def test_customer_portal_links_existing_inquiry_by_email(self):
        Contact.objects.create(
            name="Client One",
            email="client@example.com",
            phone="03001112222",
            message="Need a quote for my home.",
        )

        response = self.client.post(
            reverse("register"),
            {
                "username": "client",
                "full_name": "Client One",
                "email": "client@example.com",
                "phone": "03001112222",
                "password1": "customerpass123",
                "password2": "customerpass123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("customer-dashboard"))
        self.assertEqual(Contact.objects.filter(linked_user__username="client").count(), 1)
