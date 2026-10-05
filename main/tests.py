from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from main.forms import ExperienceForm
from main.models import Experience, Project


class ExperienceAjaxTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Volunteer Developer",
            company="UI Robotics",
            start_date=date(2025, 1, 15),
            is_active=True,
            description="Built a small robotics dashboard.",
        )
        self.admin = User.objects.create_superuser(
            username="portfolio-admin", email="admin@example.com", password="safe-test-password"
        )

    def test_experience_page_is_a_skeleton_and_visitors_can_read_json(self):
        page = self.client.get(reverse("main:show_experience"))
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, self.experience.title)
        self.assertContains(page, 'id="experience-loading"')

        response = self.client.get(reverse("main:show_json_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], self.experience.title)
        self.assertEqual(response.json()[0]["star_count"], 0)
        self.assertFalse(response.json()[0]["is_starred"])

    def test_ajax_search_matches_title_company_and_description(self):
        url = reverse("main:show_json_experience")
        self.assertEqual(len(self.client.get(url, {"search": "robotics"}).json()), 1)
        self.assertEqual(len(self.client.get(url, {"search": "unmatched"}).json()), 0)
        self.assertEqual(len(self.client.get(url, {"search": " "}).json()), 1)

    def test_add_requires_superuser_and_returns_json_validation_errors(self):
        url = reverse("main:create_experience_ajax")
        payload = {
            "title": "Product Designer",
            "company": "Campus Lab",
            "start_date": "2026-01-01",
            "description": "Designed a dashboard.",
        }
        self.assertEqual(self.client.post(url, payload).status_code, 403)

        self.client.force_login(User.objects.create_user("regular", password="test-password"))
        self.assertEqual(self.client.post(url, payload).status_code, 403)

        self.client.force_login(self.admin)
        invalid = self.client.post(url, {**payload, "start_date": "not-a-date"})
        self.assertEqual(invalid.status_code, 400)
        self.assertIn("errors", invalid.json())

        created = self.client.post(url, payload)
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["experience"]["title"], "Product Designer")
        self.assertTrue(Experience.objects.filter(title="Product Designer").exists())

    def test_experience_form_strips_html_before_saving(self):
        form = ExperienceForm(data={
            "title": "<b>Engineer</b>",
            "company": "<i>Robotics Lab</i>",
            "start_date": "2025-01-01",
            "is_active": "on",
            "description": "<img src=x onerror=alert(1)>Built a robot.",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Engineer")
        self.assertEqual(form.cleaned_data["company"], "Robotics Lab")
        self.assertNotIn("<img", form.cleaned_data["description"])

    def test_starring_is_authenticated_and_updates_count_and_status(self):
        url = reverse("main:toggle_experience_star", args=[self.experience.id])
        self.assertEqual(self.client.post(url).status_code, 403)
        self.client.force_login(User.objects.create_user("reader", password="test-password"))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_starred"])
        self.assertEqual(response.json()["star_count"], 1)
        listed = self.client.get(reverse("main:show_json_experience")).json()[0]
        self.assertTrue(listed["is_starred"])

    def test_ajax_post_is_csrf_protected(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.admin)
        url = reverse("main:create_experience_ajax")
        payload = {
            "title": "New Role",
            "company": "Test Org",
            "start_date": "2026-01-01",
            "description": "Description",
        }
        self.assertEqual(csrf_client.post(url, payload).status_code, 403)
        csrf_client.get(reverse("main:show_experience"))
        token = csrf_client.cookies["csrftoken"].value
        response = csrf_client.post(url, payload, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)

    def test_logout_redirects_and_clears_last_login_cookie(self):
        self.client.force_login(self.admin)
        self.client.cookies["last_login"] = "previous-session"
        response = self.client.get(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_existing_project_star_data_and_toggle_still_work(self):
        project = Project.objects.create(
            title="Portfolio",
            description="A portfolio site.",
            tech_stack="Django",
        )
        data_url = reverse("main:get_projects_json")
        project_data = self.client.get(data_url).json()[0]["fields"]
        self.assertEqual(project_data["star_count"], 0)
        self.assertFalse(project_data["is_starred"])

        reader = User.objects.create_user("project-reader", password="test-password")
        self.client.force_login(reader)
        response = self.client.post(reverse("main:toggle_star", args=[project.id]))
        self.assertEqual(response.status_code, 302)
        project_data = self.client.get(data_url).json()[0]["fields"]
        self.assertEqual(project_data["star_count"], 1)
        self.assertTrue(project_data["is_starred"])
