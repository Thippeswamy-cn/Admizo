from django.test import TestCase
from django.urls import reverse

from .models import Business, ContactInquiry


class HomePageTests(TestCase):
    def test_home_page_renders_and_uses_fallback_content(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Building businesses")
        self.assertContains(response, "Verified figure pending")
        self.assertContains(response, "Representative photography")
        self.assertContains(response, "work-technology.jpg")
        self.assertContains(response, "work-technology.jpg")

    def test_published_business_replaces_fallback_list(self):
        Business.objects.create(
            title="Verified Division",
            slug="verified-division",
            summary="Approved business summary.",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Verified Division")
        self.assertNotContains(response, "Other Ventures")

    def test_valid_contact_submission_is_saved(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Asha Rao",
                "email": "asha@example.com",
                "company": "Example Co",
                "phone": "+91 90000 00000",
                "service": "technology",
                "message": "We would like to discuss a new business platform.",
            },
        )
        self.assertRedirects(response, "/?sent=1#contact", fetch_redirect_response=False)
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_short_contact_message_is_rejected(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Asha",
                "email": "asha@example.com",
                "service": "technology",
                "message": "Too short",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "at least 20 characters")
        self.assertFalse(ContactInquiry.objects.exists())
