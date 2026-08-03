from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tenders.models import AlertPreference, Source, Tender
from tenders.services import notify_users_of_tender
from tenders.tender_queryset import filter_tenders

User = get_user_model()


class TenderMatchingTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="eTenders",
            slug="etenders",
            base_url="https://www.etenders.gov.za/",
            scraper_name="etenders",
        )
        self.tender = Tender.objects.create(
            source=self.source,
            external_id="match-1",
            title="Office cleaning services Gauteng",
            description="Deep cleaning for municipal buildings",
            department="City of Johannesburg",
            province="Gauteng",
            closing_date=date.today() + timedelta(days=14),
            url="https://example.com/tender/1",
        )

    def test_alert_preference_keyword_match_sends_email(self):
        user = User.objects.create_user(
            username="matcher", email="matcher@example.com", password="pass"
        )
        AlertPreference.objects.create(user=user, keywords="cleaning", delivery_email=True)

        notify_users_of_tender(self.tender)

        self.assertEqual(user.alert_events.count(), 1)
        self.assertEqual(user.alert_events.first().status, "sent")


class TenderQuerysetTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="eTenders",
            slug="etenders",
            base_url="https://www.etenders.gov.za/",
            scraper_name="etenders",
        )
        today = timezone.localdate()
        Tender.objects.create(
            source=self.source,
            external_id="open-1",
            title="Open tender",
            url="https://example.com/open",
            closing_date=today + timedelta(days=10),
        )
        Tender.objects.create(
            source=self.source,
            external_id="expired-1",
            title="Expired tender",
            url="https://example.com/expired",
            closing_date=today - timedelta(days=1),
        )

    def test_open_date_filter_excludes_expired(self):
        qs = filter_tenders(date_filter="open")
        titles = list(qs.values_list("title", flat=True))
        self.assertIn("Open tender", titles)
        self.assertNotIn("Expired tender", titles)
