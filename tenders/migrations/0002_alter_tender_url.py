from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tender",
            name="url",
            field=models.URLField(max_length=500),
        ),
    ]
