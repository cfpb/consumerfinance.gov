from datetime import date
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy
from wagtail.wagtailcore.models import Page

from cfgov.test import HtmlMixin
from jobmanager.models.blocks import JobListingList, JobListingTable
from jobmanager.models.django import Grade, JobCategory, Location
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel, RegionPanel
from scripts._atomic_helpers import job_listing_list
from v1.models import SublandingPage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


def make_job_listing_page(title, close_date=None, grades=[], regions=[],
                          **kwargs):
    page = mommy.prepare(
        JobListingPage,
        title=title,
        close_date=close_date or timezone.now().date(),
        description='description',
        division=mommy.make(JobCategory),
        **kwargs
    )

    home = Page.objects.get(slug='cfgov')
    home.add_child(instance=page)

    for grade in grades:
        grade_model = mommy.make(Grade, grade=grade)
        GradePanel.objects.create(grade=grade_model, job_listing=page)

    for region in regions:
        region_model = mommy.make(Location, region_long=region)
        RegionPanel.objects.create(region=region_model, job_listing=page)

    return page


class JobListingListTestCase(HtmlMixin, TestCase):
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
            close_date=date(2099, 8, 5),
            regions=['NY', 'DC']
        )

        block = JobListingList()
        html = block.render(block.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<ul class="list list__unstyled">.*</ul>'
        ))

    def test_html_formatting(self):
        make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2099, 8, 5),
            regions=['NY', 'DC']
        )
        make_job_listing_page(
            title='Assistant',
            grades=['12'],
            close_date=date(2099, 4, 21),
            regions=['Silicon Valley']
        )

        block = JobListingList()
        html = block.render(block.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<li class="list_item">'
            '<a class="list_link" href=".*">Assistant</a>'
            '<p class="date">CLOSING<span class="datetime">'
            '.*APR 21, 2099.*</span></p>'
            '</li>'
            '<li class="list_item">'
            '<a class="list_link" href=".*">Manager</a>'
            '<p class="date">CLOSING<span class="datetime">.'
            '*AUG 05, 2099.*</span></p>'
            '</li>'
        ))

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False, shared=False)
        qs = JobListingList().get_queryset({})
        self.assertFalse(qs.exists())

    def test_excludes_shared_jobs(self):
        make_job_listing_page('Job', live=False, shared=True)
        qs = JobListingList().get_queryset({})
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True, shared=False)
        qs = JobListingList().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)

    def test_includes_live_and_shared_jobs(self):
        job = make_job_listing_page('Job', live=True, shared=True)
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
    def test_html_has_table(self):
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '^<table class="o-table table__stack-on-small">'
            '.*'
            '</table>$'
        ))

    def test_html_has_header(self):
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<thead>'
            '<tr>'
            '<th scope="col">TITLE</th>'
            '<th scope="col">GRADE</th>'
            '<th scope="col">POSTING CLOSES</th>'
            '<th scope="col">REGION</th>'
            '</tr>'
            '</thead>'
        ))

    def test_html_formatting(self):
        make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2099, 8, 5),
            regions=['NY', 'DC']
        )
        make_job_listing_page(
            title='Assistant',
            grades=['12'],
            close_date=date(2099, 4, 21),
            regions=['Silicon Valley']
        )

        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE"><a href=".*">Assistant</a></td>'
            '<td data-label="GRADE">12</td>'
            '<td data-label="POSTING CLOSES">APR 21, 2099</td>'
            '<td data-label="REGION">Silicon Valley</td>'
            '</tr>'
            '<tr>'
            '<td data-label="TITLE"><a href=".*">Manager</a></td>'
            '<td data-label="GRADE">1, 2, 3</td>'
            '<td data-label="POSTING CLOSES">AUG 05, 2099</td>'
            '<td data-label="REGION">DC, NY</td>'
            '</tr>'
        ))

    def test_html_formatting_no_grade_or_region(self):
        make_job_listing_page(
            title='CEO',
            close_date=date(2099, 12, 1)
        )

        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE"><a href=".*">CEO</a></td>'
            '<td data-label="GRADE"></td>'
            '<td data-label="POSTING CLOSES">DEC 01, 2099</td>'
            '<td data-label="REGION"></td>'
            '</tr>'
        ))

    def test_excludes_draft_jobs(self):
        make_job_listing_page('Job', live=False, shared=False)
        qs = JobListingTable().get_queryset({})
        self.assertFalse(qs.exists())

    def test_excludes_shared_jobs(self):
        make_job_listing_page('Job', live=False, shared=True)
        qs = JobListingTable().get_queryset({})
        self.assertFalse(qs.exists())

    def test_includes_live_jobs(self):
        job = make_job_listing_page('Job', live=True, shared=False)
        qs = JobListingTable().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)

    def test_includes_live_and_shared_jobs(self):
        job = make_job_listing_page('Job', live=True, shared=True)
        qs = JobListingTable().get_queryset({})
        self.assertTrue(qs.exists())
        self.assertEqual(job.title, qs[0].title)
