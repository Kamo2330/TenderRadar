from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenders", "0002_alter_tender_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="tender",
            name="tender_type",
            field=models.CharField(
                choices=[
                    ("unknown", "Unknown / unclassified"),
                    ("socs", "SOCs Tenders"),
                    ("municipality", "Municipality Tenders"),
                    ("university", "University Tenders"),
                    ("tvet_colleges", "TVET Colleges Tenders"),
                    ("private_company", "Private Company Tenders"),
                    ("government_department", "Government Department Tenders"),
                ],
                db_index=True,
                default="unknown",
                help_text="High-level classification (buyer/org heuristics + API hints).",
                max_length=40,
            ),
        ),
    ]
