from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "One-time schema fix for legacy databases created without migrations."

    def handle(self, *args, **options):
        if connection.vendor != "sqlite":
            self.stdout.write(
                self.style.WARNING(
                    f"Unsupported DB vendor for this fixer: {connection.vendor}"
                )
            )
            return

        with connection.cursor() as cursor:
            # 1) Add tenders_client.is_managed if missing
            cursor.execute("PRAGMA table_info(tenders_client)")
            cols = {row[1] for row in cursor.fetchall()}  # row[1] = column name
            if "is_managed" not in cols:
                self.stdout.write("Adding column tenders_client.is_managed ...")
                cursor.execute(
                    "ALTER TABLE tenders_client ADD COLUMN is_managed bool NOT NULL DEFAULT 0"
                )
            else:
                self.stdout.write("Column tenders_client.is_managed already exists.")

            # 2) Create tenders_tenderapplication if missing
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tenders_tenderapplication'"
            )
            exists = cursor.fetchone() is not None
            if not exists:
                self.stdout.write("Creating table tenders_tenderapplication ...")
                cursor.execute(
                    """
                    CREATE TABLE tenders_tenderapplication (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        status varchar(30) NOT NULL DEFAULT 'not_submitted',
                        submitted_at datetime NULL,
                        notes text NOT NULL DEFAULT '',
                        created_at datetime NOT NULL,
                        updated_at datetime NOT NULL,
                        client_id bigint NOT NULL REFERENCES tenders_client(id) DEFERRABLE INITIALLY DEFERRED,
                        tender_id bigint NOT NULL REFERENCES tenders_tender(id) DEFERRABLE INITIALLY DEFERRED,
                        UNIQUE(client_id, tender_id)
                    )
                    """
                )
                cursor.execute(
                    "CREATE INDEX tenders_tenderapplication_client_id_idx ON tenders_tenderapplication(client_id)"
                )
                cursor.execute(
                    "CREATE INDEX tenders_tenderapplication_tender_id_idx ON tenders_tenderapplication(tender_id)"
                )
            else:
                self.stdout.write("Table tenders_tenderapplication already exists.")

            # 3) tenders_tender.tender_type (classifier labels)
            cursor.execute("PRAGMA table_info(tenders_tender)")
            tcols = {row[1] for row in cursor.fetchall()}
            if "tender_type" not in tcols:
                self.stdout.write("Adding column tenders_tender.tender_type ...")
                cursor.execute(
                    "ALTER TABLE tenders_tender ADD COLUMN tender_type varchar(40) NOT NULL DEFAULT 'unknown'"
                )
            else:
                self.stdout.write("Column tenders_tender.tender_type already exists.")

        self.stdout.write(self.style.SUCCESS("Schema fix complete."))

