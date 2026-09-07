from django.db import models


class OrderedContent(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")


class Business(OrderedContent):
    ACCENT_CHOICES = [
        ("blue", "Technology blue"),
        ("green", "Growth green"),
        ("orange", "Action orange"),
    ]

    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=240)
    image = models.ImageField(
        upload_to="businesses/",
        blank=True,
        help_text="Optional approved card background. A curated fallback is used when empty.",
    )
    icon = models.CharField(
        max_length=32,
        default="grid",
        help_text="Icon key: grid, building, signal, chart, or compass.",
    )
    accent = models.CharField(max_length=12, choices=ACCENT_CHOICES, default="blue")

    class Meta(OrderedContent.Meta):
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.title


class CompanyMetric(OrderedContent):
    value = models.CharField(max_length=16, help_text="Example: 10+")
    label = models.CharField(max_length=60)
    note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.value} {self.label}"


class Project(OrderedContent):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    summary = models.CharField(max_length=260)
    image = models.ImageField(upload_to="projects/", blank=True)
    case_study_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Insight(OrderedContent):
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=60, default="Perspective")
    summary = models.CharField(max_length=260)
    published_on = models.DateField(blank=True, null=True)
    external_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class ContactInquiry(models.Model):
    SERVICE_CHOICES = [
        ("technology", "Technology"),
        ("real-estate", "Real estate"),
        ("promotions", "Promotions"),
        ("business-development", "Business development"),
        ("other", "Other venture"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=32, choices=SERVICE_CHOICES)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.get_service_display()}"
