from datetime import timedelta

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from wagtail.core.models import Site
from wagtail.tests.utils import WagtailTestUtils

from jobmanager.models.django import (
    Grade,
    JobCategory,
    MajorCity,
    Office,
    Region,
    State,
)
from jobmanager.models.pages import JobListingPage
from v1.models.snippets import ReusableText


class JobListingPageQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        today = timezone.now().date()
        root_page = Site.objects.get(is_default_site=True).root_page
        division = JobCategory.objects.create(job_category="Division")

        defaults = {
            "description": "description",
            "salary_min": 0,
            "salary_max": 1000,
            "division": division,
        }

        live_job = JobListingPage(
            title="Job",
            open_date=today - timedelta(days=7),
            close_date=today + timedelta(days=7),
            **defaults,
        )
        root_page.add_child(instance=live_job)

        another_live_job = JobListingPage(
            title="Another job",
            open_date=today - timedelta(days=7),
            close_date=today + timedelta(days=7),
            **defaults,
        )
        root_page.add_child(instance=another_live_job)

        expired_job = JobListingPage(
            title="Expired job",
            open_date=today - timedelta(days=7),
            close_date=today - timedelta(days=1),
            **defaults,
        )
        root_page.add_child(instance=expired_job)

    def test_open(self):
        open_jobs = JobListingPage.objects.open()
        self.assertEqual(open_jobs.count(), 2)
        self.assertSequenceEqual(
            open_jobs.values_list("title", flat=True), ["Another job", "Job"]
        )


class JobListingPageFormTests(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.division = JobCategory.objects.create(job_category="Division")

        Region.objects.create(name="Northeast region", abbreviation="NE")

        State.objects.create(name="New York", abbreviation="NY", region_id="NE")

        Office.objects.create(abbreviation="NY", name="New York", state_id="NY")

        self.login()

    def test_page_creation_success_with_office(self):
        response = self.create_page(offices=["NY"])
        self.assertEqual(response.status_code, 302)

        try:
            JobListingPage.objects.get(
                path__startswith=self.root_page.path, slug="test-job-page"
            )
        except JobListingPage.DoesNotExist:  # pragma: nocover
            self.fail("Job listing page should be successfully created")

    def test_page_creation_fails_without_offices_or_regions(self):
        response = self.create_page()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The page could not be created")
        self.assertContains(response, "one or more offices", 2)

    def test_page_creation_fails_with_both_offices_and_regions(self):
        response = self.create_page(offices=["NY"], regions=["NE"])

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The page could not be created")
        self.assertContains(response, "one or more offices", 2)

    def test_page_creation_fails_with_regions_and_remote(self):
        response = self.create_page(regions=["NE"], allow_remote=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The page could not be created")
        self.assertContains(response, "Remote option only applies")

    def create_page(self, **kwargs):
        description_field = JobListingPage._meta.get_field("description")
        description_editor = description_field.formfield().widget
        test_description = description_editor.format_value("Test description")
        post_data = {
            "title": "Test job page",
            "slug": "test-job-page",
            "description": test_description,
            "open_date": "2099-01-01",
            "close_date": "2099-12-01",
            "salary_min": 1,
            "salary_max": 100,
            "division": self.division.pk,
            "categories-INITIAL_FORMS": 0,
            "categories-TOTAL_FORMS": 0,
            "grades-INITIAL_FORMS": 0,
            "grades-TOTAL_FORMS": 0,
            "email_application_links-INITIAL_FORMS": 0,
            "email_application_links-TOTAL_FORMS": 0,
            "usajobs_application_links-INITIAL_FORMS": 0,
            "usajobs_application_links-TOTAL_FORMS": 0,
            "language": "en",
            "schema_json": "null",
            "is_archived": "no",
        }

        post_data.update(kwargs)

        return self.client.post(
            reverse(
                "wagtailadmin_pages:add",
                args=("jobmanager", "joblistingpage", self.root_page.id),
            ),
            post_data,
        )


class JobListingPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = HttpRequest()

        cls.grade = Grade.objects.create(grade="53", salary_min=1, salary_max=100)

        cls.northeast = Region.objects.create(
            name="Northeast region", abbreviation="NE"
        )

        State.objects.create(name="New York", abbreviation="NY", region_id="NE")

        cls.new_york = Office.objects.create(
            abbreviation="NY", name="New York", state_id="NY"
        )

        cls.major_city = MajorCity.objects.create(
            name="Albany", state_id="NY", region_id="NE"
        )

    def test_get_context_empty_page(self):
        page = JobListingPage()
        context = page.get_context(self.request)

        self.assertEqual(context["offices"], [])
        self.assertEqual(context["regions"], [])
        self.assertEqual(context["grades"], [])

        self.assertNotIn("about_us", context)

    def test_get_context_with_about_us_snippet(self):
        about_us = ReusableText.objects.create(title="About us (For consumers)")

        page = JobListingPage()
        context = page.get_context(self.request)

        self.assertEqual(context["about_us"], about_us)

    def test_get_context_all_fields(self):
        page = JobListingPage(
            offices=[self.new_york],
            regions=[self.northeast],
            grades=[self.grade],
        )

        context = page.get_context(self.request)

        self.assertEqual(
            context["offices"],
            [
                {
                    "name": "New York",
                    "state_id": "NY",
                },
            ],
        )

        self.assertEqual(
            context["regions"],
            [
                {
                    "name": "Northeast region",
                    "states": ["NY"],
                    "major_cities": [
                        {
                            "name": "Albany",
                            "state_id": "NY",
                        },
                    ],
                },
            ],
        )

        self.assertEqual(context["grades"], ["53"])

    def test_page_includes_extra_js(self):
        self.assertIn("summary.js", JobListingPage().page_js)
