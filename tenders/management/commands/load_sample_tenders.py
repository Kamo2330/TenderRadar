from django.core.management.base import BaseCommand

from tenders.models import Source, Tender
from tenders.sample_data import SAMPLE_SOURCES, SAMPLE_TENDERS


class Command(BaseCommand):
    help = "Load sample South African tenders for local development and demos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove existing sample tenders (external_id starts with 'sample-') before loading.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Tender.objects.filter(external_id__startswith="sample-").delete()
            self.stdout.write(f"Removed {deleted} existing sample tender(s).")

        sources = {}
        for source_data in SAMPLE_SOURCES:
            source, created = Source.objects.update_or_create(
                slug=source_data["slug"],
                defaults={
                    "name": source_data["name"],
                    "base_url": source_data["base_url"],
                    "scraper_name": source_data["scraper_name"],
                    "is_active": True,
                },
            )
            sources[source.slug] = source
            if created:
                self.stdout.write(f"Created source: {source.name}")

        created_count = 0
        updated_count = 0
        for row in SAMPLE_TENDERS:
            source = sources[row["source_slug"]]
            _, created = Tender.objects.update_or_create(
                source=source,
                external_id=row["external_id"],
                defaults={
                    "title": row["title"],
                    "description": row["description"],
                    "department": row["department"],
                    "category": row["category"],
                    "tender_type": row["tender_type"],
                    "province": row["province"],
                    "published_date": row["published_date"],
                    "closing_date": row["closing_date"],
                    "url": row["url"],
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        total = Tender.objects.filter(external_id__startswith="sample-").count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Sample tenders ready: {created_count} created, {updated_count} updated "
                f"({total} total sample records)."
            )
        )
