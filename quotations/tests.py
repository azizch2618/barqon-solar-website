from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import CompanyProfile
from .models import Quotation


User = get_user_model()


class QuotationApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="strongpass123",
            is_admin=True,
            is_staff=True,
        )
        CompanyProfile.objects.create(company_name="BARQON Solar Solutions")

    def test_owner_can_create_quotation(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            reverse("quotation-list"),
            {
                "customer_name": "Ali Khan",
                "customer_email": "ali@example.com",
                "customer_phone": "03001234567",
                "address": "Lahore",
                "project_title": "10kW Hybrid System",
                "system_size": 10,
                "panel_capacity_kw": "10.00",
                "inverter": "Hybrid Inverter",
                "inverter_size_kw": "8.00",
                "battery": "Lithium Battery Bank",
                "battery_size_kwh": "15.00",
                "subtotal": "1800000.00",
                "discount": "50000.00",
                "tax_amount": "0.00",
                "total_cost": "1750000.00",
                "notes": "Includes installation.",
                "status": "draft",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quotation.objects.count(), 1)
        quotation = Quotation.objects.first()
        self.assertTrue(quotation.quotation_number.startswith("BARQON-"))
        self.assertEqual(quotation.total_cost, Decimal("1750000.00"))

    def test_owner_can_download_pdf(self):
        quotation = Quotation.objects.create(
            customer_name="Ali Khan",
            address="Lahore",
            system_size=10,
            inverter="Hybrid Inverter",
            battery="Lithium Battery Bank",
            total_cost=Decimal("1750000.00"),
            prepared_by=self.owner,
        )
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(reverse("quotation-pdf", args=[quotation.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_owner_can_open_frontend_quotation_form(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("owner-quotation-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Create Quotation")

    def test_customer_can_view_and_download_linked_quotation(self):
        customer = User.objects.create_user(
            username="customer",
            password="customerpass123",
            email="customer@example.com",
        )
        quotation = Quotation.objects.create(
            customer_name="Customer One",
            customer_email="customer@example.com",
            address="Lahore",
            system_size=10,
            inverter="Hybrid Inverter",
            battery="Lithium Battery Bank",
            total_cost=Decimal("1750000.00"),
            prepared_by=self.owner,
        )

        self.client.force_login(customer)
        dashboard_response = self.client.get(reverse("customer-dashboard"))
        pdf_response = self.client.get(reverse("customer-quotation-pdf", args=[quotation.id]))

        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        self.assertContains(dashboard_response, quotation.quotation_number)
        self.assertEqual(pdf_response.status_code, status.HTTP_200_OK)
