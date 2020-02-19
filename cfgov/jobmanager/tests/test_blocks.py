from datetime import date

from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.utils.encoding import force_text

from mock import Mock
from model_mommy import mommy
from scripts._atomic_helpers import job_listing_list

from jobmanager.blocks import JobListingList, JobListingTable
from jobmanager.models.django import Grade, JobCategory, JobLocation
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel
from v1.models import SublandingPage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


try:
    from wagtail.core.models import Page
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.models import Page


def make_job_listing_page(title, close_date=None, grades=[], **kwargs):
    page = mommy.prepare(
        JobListingPage,
        title=title,
        close_date=close_date or timezone.now().date(),
        description='description',
        division=mommy.make(JobCategory),
        location=mommy.make(JobLocation, name='Silicon Valley'),
        **kwargs
    )

    home = Page.objects.get(slug='cfgov')
    home.add_child(instance=page)

    for grade in grades:
        grade_model = mommy.make(Grade, grade=grade)
        GradePanel.objects.create(grade=grade_model, job_listing=page)

    return page


class JobListingListTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.more_jobs_page = Page.objects.first()

    def _render_block_to_html(self):
        block = JobListingList()
        return block.render(block.to_python({
            'more_jobs_page': self.more_jobs_page.pk,
        }))

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
        qs = JobListingList().get_queryset({})
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True)
        qs = JobListingList().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)

    def test_page_renders_block_safely(self):
        """
        Test to make sure that a page with a jobs list block renders it
        in a safe way, meaning as raw HTML vs. as a quoted string.
        """
        page = SublandingPage(title='title', slug='slug')
        save_new_page(page)
        set_stream_data(page, 'sidebar_breakout', [job_listing_list])

        request = RequestFactory().get('/')
        request.user = Mock()
        rendered_html = force_text(page.serve(request).render().content)
        self.assertInHTML(
            ('<aside class="m-jobs-list" data-qa-hook="openings-section">'
             '<h3 class="short-desc">There are no current openings at this '
             'time.</h3></aside>'),
            rendered_html
        )


class JobListingTableTestCase(TestCase):
    def test_html_displays_no_data_message(self):
        table = JobListingTable()
        html = table.render(table.to_python({'empty_table_msg': 'No Jobs'}))
        self.assertInHTML('<h3>No Jobs</h3>', html)

    def test_html_displays_table_if_row_flag_false(self):
        table = JobListingTable()
        html = table.render(table.to_python(
            {'first_row_is_table_header': False}
        ))
        self.assertNotIn('<thead>', html)
        self.assertIn('TITLE', html)
        self.assertIn('GRADE', html)
        self.assertIn('POSTING CLOSES', html)
        self.assertIn('LOCATION', html)

    def test_html_has_header(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )
        table = JobListingTable()
        html = table.render(table.to_python({}))
        self.assertIn('<thead>', html)

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
        html = table.render(table.to_python({}))

        self.assertIn('Manager', html)
        self.assertIn('Assistant', html)
        self.assertIn('1, 2, 3', html)
        self.assertIn('12', html)
        self.assertIn('Aug. 5, 2099', html)
        self.assertIn('Apr. 21, 2099', html)
        self.assertEqual(html.count('Silicon Valley'), 2)

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False)
        qs = JobListingTable().get_queryset({})
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True)
        qs = JobListingTable().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)
