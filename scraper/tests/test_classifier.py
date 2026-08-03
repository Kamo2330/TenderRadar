from django.test import SimpleTestCase

from scraper.tender_type_classifier import classify_tender_type
from tenders.models import Tender


class TenderTypeClassifierTests(SimpleTestCase):
    def test_eskom_classified_as_soc(self):
        result = classify_tender_type(buyer_or_org_name="Eskom Holdings SOC Ltd")
        self.assertEqual(result, Tender.TenderType.SOCS.value)

    def test_university_classified(self):
        result = classify_tender_type(buyer_or_org_name="University of Cape Town")
        self.assertEqual(result, Tender.TenderType.UNIVERSITY.value)
