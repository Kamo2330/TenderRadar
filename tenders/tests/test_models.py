from django.contrib.auth import get_user_model
from django.test import TestCase

from tenders.models import AlertPreference, Source, Tender

User = get_user_model()


class TenderModelTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="eTenders",
            slug="etenders",
            base_url="https://www.etenders.gov.za/",
            scraper_name="etenders",
        )

    def test_tender_str_uses_title(self):
        tender = Tender.objects.create(
            source=self.source,
            external_id="ocds-123",
            title="Supply of office furniture",
            url="https://www.etenders.gov.za/example",
        )
        self.assertEqual(str(tender), "Supply of office furniture")


class AlertPreferenceTests(TestCase):
    def test_keyword_list_parses_csv(self):
        user = User.objects.create_user(username="biz", password="pass")
        prefs = AlertPreference.objects.create(
            user=user,
            keywords="cleaning, security , IT",
        )
        self.assertEqual(prefs.keyword_list(), ["cleaning", "security", "IT"])
