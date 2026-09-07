from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("website", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="business",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Optional approved card background. A curated fallback is used when empty.",
                upload_to="businesses/",
            ),
        ),
    ]
