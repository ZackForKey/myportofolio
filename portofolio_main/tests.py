from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Experience


class PortfolioRoutingTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Computer Science Student",
            company="Fasilkom UI",
            start_date=date(2025, 9, 1),
            is_active=True,
            description="Studying web development and Django.",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        self.assertEqual(self.client.get("/halaman-yang-tidak-ada/").status_code, 404)

    def test_experience_page_uses_ajax_skeleton_and_json_endpoint(self):
        page = self.client.get(reverse("main:show_experience"))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "experience.html")
        self.assertNotContains(page, self.experience.title)
        self.assertContains(page, 'id="experience-loading"')

        data = self.client.get(reverse("main:show_json_experience")).json()
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertTrue(data[0]["is_active"])

    def test_empty_experience_state_is_present(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan atau ditemukan.")

    def test_completed_experience_is_returned_as_inactive(self):
        self.experience.is_active = False
        self.experience.save()
        data = self.client.get(reverse("main:show_json_experience")).json()
        self.assertFalse(data[0]["is_active"])
