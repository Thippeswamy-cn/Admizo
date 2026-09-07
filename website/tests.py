from django.test import TestCase
from django.urls import reverse

from .models import Business, ContactInquiry
from .views import FALLBACK_BUSINESSES


class BusinessPageTests(TestCase):
    def test_directory_and_fallback_detail_links(self):
        for page in [reverse("home"), reverse("business_list")]:
            response = self.client.get(page)
            for business in FALLBACK_BUSINESSES:
                url = reverse("business_detail", args=[business["slug"]])
                self.assertContains(response, f'href="{url}"')
        for business in FALLBACK_BUSINESSES:
            response = self.client.get(reverse("business_detail", args=[business["slug"]]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'businesses/{business["slug"]}/index.html')
            self.assertContains(response, business["summary"])
            self.assertContains(response, 'href="/#contact"')

    def test_custom_business_and_unpublished_business(self):
        business = Business.objects.create(title="Consulting", slug="consulting", summary="Approved consulting services.")
        url = reverse("business_detail", args=[business.slug])
        self.assertContains(self.client.get(url), business.summary)
        business.is_published = False
        business.save()
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_unknown_business_returns_404(self):
        self.assertEqual(self.client.get('/businesses/unknown/').status_code, 404)


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
