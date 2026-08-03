from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tenders.models import Source, Tender

User = get_user_model()


class TenderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="secret")
        self.source = Source.objects.create(
            name="eTenders",
            slug="etenders",
            base_url="https://www.etenders.gov.za/",
            scraper_name="etenders",
        )
        Tender.objects.create(
            source=self.source,
            external_id="api-1",
            title="Security services tender",
            url="https://example.com/security",
            closing_date=date.today() + timedelta(days=7),
        )

    def test_login_returns_token(self):
        response = self.client.post(
            reverse("api_login"),
            {"username": "apiuser", "password": "secret"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_tender_list_requires_auth(self):
        response = self.client.get(reverse("api_tender_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tender_list_returns_results_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("api_tender_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class RegisterAPITests(APITestCase):
    def test_register_creates_user_and_returns_token(self):
        response = self.client.post(
            reverse("api_register"),
            {
                "username": "newbiz",
                "email": "newbiz@example.com",
                "password": "securepass123",
                "company_name": "New Biz Pty Ltd",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "newbiz")
        self.assertTrue(
            User.objects.filter(username="newbiz").exists()
        )

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(username="taken", password="pass12345")
        response = self.client.post(
            reverse("api_register"),
            {
                "username": "taken",
                "email": "other@example.com",
                "password": "securepass123",
                "company_name": "Other Co",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

