from django.core.management.base import BaseCommand
from django.db import connection, transaction

from scraper.etenders import EtendersScraper
from scraper.tenders_sa import TendersSAScraper
from tenders.models import Source, Tender
from tenders.services import notify_users_of_tender


def _ensure_sqlite_tender_type_column(stdout, style) -> None:
    """Add tenders_tender.tender_type if missing (legacy DBs without migration 0003)."""
    if connection.vendor != "sqlite":
        return
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(tenders_tender)")
        cols = {row[1] for row in cursor.fetchall()}
        if "tender_type" in cols:
            return
        stdout.write("Adding missing column tenders_tender.tender_type ...")
        cursor.execute(
            "ALTER TABLE tenders_tender ADD COLUMN tender_type varchar(40) NOT NULL DEFAULT 'unknown'"
        )
        stdout.write(style.SUCCESS("Column tenders_tender.tender_type added."))


class Command(BaseCommand):
    help = (
        "Ingest tenders from real sources: National Treasury OCDS API (eTenders) "
        "and Tenders-SA aggregator API."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            choices=["etenders", "tenders_sa", "all"],
            default="all",
            help="Which scraper to run (default: all).",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="OCDS date window: today minus N days through today (eTenders only).",
        )
        parser.add_argument(
            "--ocds-page-size",
            type=int,
            default=100,
            help="OCDS API PageSize (max 1000; browser limit lower).",
        )
        parser.add_argument(
            "--ocds-max-pages",
            type=int,
            default=50,
            help="Max OCDS pages to follow via links.next (safety cap).",
        )
        parser.add_argument(
            "--tsa-max-pages",
            type=int,
            default=20,
            help="Max Tenders-SA API pages to fetch.",
        )
        parser.add_argument(
            "--tsa-page-size",
            type=int,
            default=50,
            help="Tenders-SA limit per page (max ~100).",
        )

    def handle(self, *args, **options):
        _ensure_sqlite_tender_type_column(self.stdout, self.style)

        source_arg = options["source"]
        self.stdout.write(self.style.MIGRATE_HEADING("Starting tender scrape..."))

        scrapers = []
        if source_arg in ("etenders", "all"):
            scrapers.append(
                (
                    EtendersScraper(
                        days_back=options["days"],
                        max_pages=options["ocds_max_pages"],
                        page_size=options["ocds_page_size"],
                    ),
                    {
                        "name": "SA eTenders (National Treasury OCDS)",
                        "base_url": "https://www.etenders.gov.za/",
                    },
                )
            )
        if source_arg in ("tenders_sa", "all"):
            scrapers.append(
                (
                    TendersSAScraper(
                        max_pages=options["tsa_max_pages"],
                        page_size=options["tsa_page_size"],
                    ),
                    {
                        "name": "Tenders-SA (aggregator / RFQs)",
                        "base_url": "https://www.tenders-sa.org/",
                    },
                )
            )

        total_created = 0
        total_updated = 0

        for scraper, meta in scrapers:
            source, _ = Source.objects.get_or_create(
                slug=scraper.source_slug,
                defaults={
                    "name": meta["name"],
                    "base_url": meta["base_url"],
                    "scraper_name": scraper.source_slug,
                },
            )
            # Keep metadata fresh if slug already existed (e.g. old "Demo" name).
            Source.objects.filter(pk=source.pk).update(
                name=meta["name"],
                base_url=meta["base_url"],
                scraper_name=scraper.source_slug,
            )
            source.refresh_from_db()

            created_count = 0
            updated_count = 0
            for item in scraper.fetch_tenders():
                with transaction.atomic():
                    tender, created = Tender.objects.update_or_create(
                        source=source,
                        external_id=item["external_id"],
                        defaults=item,
                    )
                if created:
                    created_count += 1
                    notify_users_of_tender(tender)
                else:
                    updated_count += 1

            total_created += created_count
            total_updated += updated_count
            self.stdout.write(
                f"  [{scraper.source_slug}] created={created_count} updated={updated_count}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Scrape complete. Total created: {total_created}, updated: {total_updated}"
            )
        )
