from datetime import date

from django.test import RequestFactory, TestCase
from django.utils import timezone

from wagtail.core.models import Page

from model_bakery import baker
from scripts._atomic_helpers import job_listing_list

from jobmanager.blocks import JobListingList, JobListingTable
from jobmanager.models.django import Grade, JobCategory, JobLocation
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel
from v1.models import SublandingPage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


try:
    from django.utils.encoding import force_str
except ImportError:
    from django.utils.encoding import force_text as force_str


def make_job_listing_page(title, close_date=None, grades=[], **kwargs):
    page = baker.prepare(
        JobListingPage,
        title=title,
        close_date=close_date or timezone.now().date(),
        description='description',
        division=baker.make(JobCategory),
        location=baker.make(JobLocation, name='Silicon Valley'),
        **kwargs
    )

    home = Page.objects.get(slug='cfgov')
    home.add_child(instance=page)

    for grade in grades:
        grade_model = baker.make(Grade, grade=grade)
        GradePanel.objects.create(grade=grade_model, job_listing=page)

    return page


class JobListingListTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.more_jobs_page = Page.objects.first()

    def get_value(self, block):
        return block.to_python({
            'more_jobs_page': self.more_jobs_page.pk,
        })

    def _render_block_to_html(self):
        block = JobListingList()
        return block.render(self.get_value(block))

    def test_html_has_aside(self):
        self.assertInHTML(
            ('<aside class="m-jobs-list" data-qa-hook="openings-section">'
             '<h3 class="short-desc">There are no current openings at this '
             'time.</h3></aside>'),
            self._render_block_to_html()
        )

    def test_html_has_job_listings(self):
        make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2099, 8, 5)
        )
        make_job_listing_page(
            title='Assistant',
            grades=['12'],
            close_date=date(2099, 4, 21)
        )
        content = self._render_block_to_html()
        self.assertIn('Assistant', content)
        self.assertIn('Manager', content)
        self.assertIn('Apr. 21, 2099', content)
        self.assertIn('Aug. 5, 2099', content)

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False)
        self.assertFalse(JobListingList().get_job_listings().exists())

    def test_includes_live_jobs(self):
        make_job_listing_page('Job', live=True)
        jobs = JobListingList().get_job_listings()
        self.assertEqual(jobs.count(), 1)
        self.assertEqual(jobs[0].title, 'Job')

    def test_page_renders_block_safely(self):
        """
        Test to make sure that a page with a jobs list block renders it
        in a safe way, meaning as raw HTML vs. as a quoted string.
        """
        page = SublandingPage(title='title', slug='slug')
        save_new_page(page)
        set_stream_data(page, 'sidebar_breakout', [job_listing_list])

        request = RequestFactory().get('/')
        rendered_html = force_str(page.serve(request).render().content)
        self.assertInHTML(
            ('<aside class="m-jobs-list" data-qa-hook="openings-section">'
             '<h3 class="short-desc">There are no current openings at this '
             'time.</h3></aside>'),
            rendered_html
        )


class JobListingTableTestCase(TestCase):
    def test_html_displays_no_data_message(self):
        self.assertInHTML(
            '<h3>There are no current openings at this time.</h3>',
            JobListingTable().render({})
        )

    def test_html_has_header(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )
        html = JobListingTable().render({})

        self.assertIn('<thead>', html)
        self.assertIn('TITLE', html)
        self.assertIn('GRADE', html)
        self.assertIn('POSTING CLOSES', html)
        self.assertIn('LOCATION', html)

    def test_html_has_job_listings(self):
        make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2099, 8, 5)
        )
        make_job_listing_page(
            title='Assistant',
            grades=['12'],
            close_date=date(2099, 4, 21)
        )

        table = JobListingTable()
        html = table.render({})

        self.assertIn('Manager', html)
        self.assertIn('Assistant', html)
        self.assertIn('1, 2, 3', html)
        self.assertIn('12', html)
        self.assertIn('Aug. 5, 2099', html)
        self.assertIn('Apr. 21, 2099', html)
        self.assertEqual(html.count('Silicon Valley'), 2)

    def test_is_efficient(self):
        for i in range(10):
            make_job_listing_page(
                title='Manager',
                grades=['1', '2', '3'],
                close_date=date(2099, 8, 5)
            )

        request = RequestFactory().get('/')

        # We expect four database queries here. First, Wagtail has to look up
        # the site root paths. These get cached on the request object. Then,
        # all of the JobListingPages are retrieved in a single query. Finally,
        # two additional queries are needed to pull back job grades.
        with self.assertNumQueries(4):
            JobListingTable().render({}, context={'request': request})

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False)
        qs = JobListingTable().get_job_listings()
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True)
        qs = JobListingTable().get_job_listings()
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)
