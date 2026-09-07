from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Business",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=80)),
                ("slug", models.SlugField(unique=True)),
                ("summary", models.CharField(max_length=240)),
                ("icon", models.CharField(default="grid", help_text="Icon key: grid, building, signal, chart, or compass.", max_length=32)),
                ("accent", models.CharField(choices=[("blue", "Technology blue"), ("green", "Growth green"), ("orange", "Action orange")], default="blue", max_length=12)),
            ],
            options={"verbose_name_plural": "Businesses", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="CompanyMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("value", models.CharField(help_text="Example: 10+", max_length=16)),
                ("label", models.CharField(max_length=60)),
                ("note", models.CharField(blank=True, max_length=100)),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="ContactInquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("company", models.CharField(blank=True, max_length=120)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("service", models.CharField(choices=[("technology", "Technology"), ("real-estate", "Real estate"), ("promotions", "Promotions"), ("business-development", "Business development"), ("other", "Other venture")], max_length=32)),
                ("message", models.TextField(max_length=2000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_reviewed", models.BooleanField(default=False)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="Insight",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=160)),
                ("category", models.CharField(default="Perspective", max_length=60)),
                ("summary", models.CharField(max_length=260)),
                ("published_on", models.DateField(blank=True, null=True)),
                ("external_url", models.URLField(blank=True)),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=120)),
                ("category", models.CharField(max_length=80)),
                ("summary", models.CharField(max_length=260)),
                ("image", models.ImageField(blank=True, upload_to="projects/")),
                ("case_study_url", models.URLField(blank=True)),
            ],
            options={"ordering": ("order", "id")},
        ),
    ]
