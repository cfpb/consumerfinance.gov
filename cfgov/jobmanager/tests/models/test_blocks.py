from datetime import date

from django.test import TestCase
from django.utils import timezone

from wagtail.wagtailcore.models import Page, Site

from mock import Mock
from model_mommy import mommy
from scripts._atomic_helpers import job_listing_list

from cfgov.test import HtmlMixin
from jobmanager.models.blocks import JobListingList, JobListingTable
from jobmanager.models.django import Grade, JobCategory, JobLocation
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel
from v1.models import SublandingPage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


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


class JobListingListTestCase(HtmlMixin, TestCase):
    def setUp(self):
        self.request = Mock(site=Site.objects.get(is_default_site=True))

    def test_html_has_aside(self):
        block = JobListingList()
        html = block.render(block.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '^<aside class="m-jobs-list" data-qa-hook="openings-section">'
            '.*'
            '</aside>$'
        ))

    def test_html_has_ul(self):
        make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2099, 8, 5)
        )

        block = JobListingList()
        html = block.render(
            block.to_python({}),
            context={'request': self.request}
        )

        self.assertHtmlRegexpMatches(html, (
            '<ul class="m-list m-list__unstyled m-list__links">.*</ul>'
        ))

    def test_html_formatting(self):
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

        block = JobListingList()
        html = block.render(
            block.to_python({}),
            context={'request': self.request}
        )

        self.assertHtmlRegexpMatches(html, (
            '<li class="m-list_item">'
            '<a class="m-list_link" href=".*">Assistant' +
            '<span class="m-list_link-subtext">Closing' +
            '<span class="datetime">.*Apr. 21, 2099.*</span>'
            '</span></a>'
            '</li>'
            '<li class="m-list_item">'
            '<a class="m-list_link" href=".*">Manager' +
            '<span class="m-list_link-subtext">Closing' +
            '<span class="datetime">.*Aug. 5, 2099.*</span>'
            '</span></a>'
            '</li>'
        ))

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

        self.assertPageIncludesHtml(page, (
            '><aside class="m-jobs-list" data-qa-hook="openings-section">'
            '.*'
            '</aside><'
        ))


class JobListingTableTestCase(HtmlMixin, TestCase):
    def test_html_displays_no_data_message(self):
        table = JobListingTable()
        html = table.render(table.to_python({'empty_table_msg': 'No Jobs'}))

        self.assertHtmlRegexpMatches(html, (
            '<h3>No Jobs</h3>'
        ))

    def test_html_displays_table_if_row_flag_false(self):
        table = JobListingTable()
        html = table.render(table.to_python(
            {'first_row_is_table_header': False}
        ))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td>TITLE</td>'
            '<td>GRADE</td>'
            '<td>POSTING CLOSES</td>'
            '<td>LOCATION</td>'
            '</tr>'
        ))

    def test_html_displays_single_row(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<th scope="col">TITLE</th>'
            '<th scope="col">GRADE</th>'
            '<th scope="col">POSTING CLOSES</th>'
            '<th scope="col">LOCATION</th>'
            '</tr>'
        ))

    def test_html_has_header(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<thead>'
            '<tr>'
            '<th scope="col">TITLE</th>'
            '<th scope="col">GRADE</th>'
            '<th scope="col">POSTING CLOSES</th>'
            '<th scope="col">LOCATION</th>'
            '</tr>'
            '</thead>'
        ))

    def test_html_formatting(self):
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

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE"><a class="" href=".*">Assistant</a></td>'
            '<td data-label="GRADE">12</td>'
            '<td data-label="POSTING CLOSES">Apr. 21, 2099</td>'
            '<td data-label="LOCATION">Silicon Valley</td>'
            '</tr>'
            '<tr>'
            '<td data-label="TITLE"><a class="" href=".*">Manager</a></td>'
            '<td data-label="GRADE">1, 2, 3</td>'
            '<td data-label="POSTING CLOSES">Aug. 5, 2099</td>'
            '<td data-label="LOCATION">Silicon Valley</td>'
            '</tr>'
        ))

    def test_html_formatting_no_grade(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )

        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE"><a class="" href=".*">CEO</a></td>'
            '<td data-label="GRADE"></td>'
            '<td data-label="POSTING CLOSES">Dec. 1, 2099</td>'
            '<td data-label="LOCATION">Silicon Valley</td>'
            '</tr>'
        ))

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False)
        qs = JobListingTable().get_queryset({})
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True)
        qs = JobListingTable().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)
