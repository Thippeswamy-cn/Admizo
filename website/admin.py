from django.contrib import admin
from .models import Business, CompanyMetric, ContactInquiry, Insight, Project


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("title", "accent", "order", "is_published")
    list_editable = ("order", "is_published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CompanyMetric)
class CompanyMetricAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_published")
    list_filter = ("category", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_on", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "created_at", "is_reviewed")
    list_filter = ("service", "is_reviewed", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("name", "email", "company", "phone", "service", "message", "created_at")
    list_editable = ("is_reviewed",)
