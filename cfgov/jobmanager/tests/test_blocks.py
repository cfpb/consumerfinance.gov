from datetime import date

from django.test import RequestFactory, TestCase

from wagtail.core.models import Site

from jobmanager.blocks import JobListingList, JobListingTable
from jobmanager.models.django import JobCategory
from jobmanager.models.pages import JobListingPage


class JobListingBlockTestUtils:
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.division = JobCategory.objects.create(job_category="Test")
        self.request = RequestFactory().get("/")
        Site.find_for_request(self.request)

    def make_job(self, title, live=True, close_date=None):
        page = JobListingPage(
            live=live,
            title=title,
            description="Test description",
            open_date=date(2000, 1, 1),
            close_date=close_date or date(2099, 12, 1),
            salary_min=1,
            salary_max=100,
            division=self.division,
        )

        self.root_page.add_child(instance=page)
        return page


class JobListingListTestCase(JobListingBlockTestUtils, TestCase):
    def render_block(self):
        block = JobListingList()
        value = block.to_python(
            {
                "more_jobs_page": self.root_page.pk,
            }
        )
        return block.render(value, context={"request": self.request})

    def test_no_jobs_message(self):
        self.assertIn("There are no current openings", self.render_block())

    def test_shows_jobs(self):
        self.make_job("live1")
        # This job should not show up because it is closed.
        self.make_job("live_closed", close_date=date(1970, 1, 1)),
        self.make_job("live2")
        # This job should not show up because it is not live.
        self.make_job("draft", live=False)
        self.make_job("live3")
        self.make_job("live4")
        self.make_job("live5")
        # These jobs should not appear because the list should be limited to 5.
        self.make_job("live6")
        self.make_job("live7")
        self.make_job("live8")

        html = self.render_block()

        self.assertIn("live1", html)
        self.assertNotIn("live_closed", html)
        self.assertIn("live2", html)
        self.assertNotIn("draft", html)
        self.assertIn("live3", html)
        self.assertIn("live4", html)
        self.assertIn("live5", html)
        self.assertNotIn("live6", html)
        self.assertNotIn("live7", html)
        self.assertNotIn("live8", html)

    def test_database_queries(self):
        for i in range(5):
            self.make_job(f"live{i}")

        # We expect three database queries here. First, Wagtail has to look up
        # the site root paths. These get cached on the request object. Then,
        # all of the JobListingPages are retrieved in a single query. Finally,
        # another query retrieves the URL for the "more jobs page" link.
        with self.assertNumQueries(3):
            self.render_block()


class JobListingTableTestCase(JobListingBlockTestUtils, TestCase):
    def render_block(self):
        return JobListingTable().render({}, context={"request": self.request})

    def test_no_jobs_message(self):
        self.assertIn("There are no current openings", self.render_block())

    def test_shows_jobs(self):
        self.make_job("live1")
        # This job should not show up because it is closed.
        self.make_job("live_closed", close_date=date(1970, 1, 1)),
        self.make_job("live2")
        # This job should not show up because it is not live.
        self.make_job("draft", live=False)
        self.make_job("live3")
        self.make_job("live4")
        self.make_job("live5")
        self.make_job("live6")

        html = self.render_block()

        self.assertIn("live1", html)
        self.assertNotIn("live_closed", html)
        self.assertIn("live2", html)
        self.assertNotIn("draft", html)
        self.assertIn("live3", html)
        self.assertIn("live4", html)
        self.assertIn("live5", html)
        self.assertIn("live6", html)

    def test_database_queries(self):
        for i in range(5):
            self.make_job(f"live{i}")

        # We expect 13 database queries:
        #
        # 1. Wagtail has to look up the site root paths, which get cached on
        #    the request object.
        # 2. One query to retrieve all of the job listing pages.
        # 3. One query to prefetch all of the job grades.
        # 5x2. Two additional queries per job to retrieve offices and
        #      regions.
        #
        # This could be greatly optimized (reducing to only 2 additional
        # location queries total) if django-modelcluster adds prefetch_related
        # support to ParentalManyToManyField:
        #
        # https://github.com/wagtail/django-modelcluster/issues/101
        with self.assertNumQueries(13):
            self.render_block()
