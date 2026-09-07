from django.core.management import call_command
from django.test import TestCase

from tenders.models import Source, Tender


class LoadSampleTendersTests(TestCase):
    def test_load_sample_tenders_creates_records(self):
        call_command("load_sample_tenders")
        self.assertGreaterEqual(Source.objects.count(), 2)
        self.assertGreaterEqual(Tender.objects.filter(external_id__startswith="sample-").count(), 10)

    def test_load_sample_tenders_is_idempotent(self):
        call_command("load_sample_tenders")
        count_after_first = Tender.objects.filter(external_id__startswith="sample-").count()
        call_command("load_sample_tenders")
        count_after_second = Tender.objects.filter(external_id__startswith="sample-").count()
        self.assertEqual(count_after_first, count_after_second)
