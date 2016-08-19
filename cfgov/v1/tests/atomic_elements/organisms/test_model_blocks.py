import re

from datetime import date
from model_mommy import mommy
from unittest import TestCase
from wagtail.wagtailcore.models import Page

from jobmanager.models.django import Grade, JobCategory, Location
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel, RegionPanel
from v1.atomic_elements.organisms import JobListingTable


class JobListingTableTestCase(TestCase):
    def test_init_needs_no_arguments(self):
        try:
            JobListingTable()
        except TypeError:
            self.fail('JobListingTable should require no arguments')

    def test_html_has_table(self):
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '^<table '
            'class="table__stack-on-small table__entry-header-on-small">'
            '.*'
            '</table>$'
        ))

    def test_html_has_header(self):
        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<thead>'
            '<tr>'
            '<th>TITLE</th>'
            '<th>GRADE</th>'
            '<th>POSTING CLOSES</th>'
            '<th>REGION</th>'
            '</tr>'
            '</thead>'
        ))

    def test_html_formatting(self):
        self.make_job_listing_page(
            title='Manager',
            grades=['1', '2', '3'],
            close_date=date(2016, 8, 5),
            regions=['NY', 'DC']
        )
        self.make_job_listing_page(
            title='Assistant',
            grades=['12'],
            close_date=date(2016, 4, 21),
            regions=['Silicon Valley']
        )

        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE">Assistant</td>'
            '<td data-label="GRADE">12</td>'
            '<td data-label="POSTING CLOSES">APR 21, 2016</td>'
            '<td data-label="REGION">Silicon Valley</td>'
            '</tr>'
            '<tr>'
            '<td data-label="TITLE">Manager</td>'
            '<td data-label="GRADE">1, 2, 3</td>'
            '<td data-label="POSTING CLOSES">AUG 05, 2016</td>'
            '<td data-label="REGION">DC, NY</td>'
            '</tr>'
        ))

    def test_html_formatting_no_grade_or_region(self):
        self.make_job_listing_page(
            title='CEO',
            close_date=date(2016, 12, 1)
        )

        table = JobListingTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="TITLE">CEO</td>'
            '<td data-label="GRADE"></td>'
            '<td data-label="POSTING CLOSES">DEC 01, 2016</td>'
            '<td data-label="REGION"></td>'
            '</tr>'
        ))

    @staticmethod
    def make_job_listing_page(title, close_date, grades=[], regions=[]):
        page = mommy.prepare(
            JobListingPage,
            title=title,
            close_date=close_date,
            description='description',
            division=mommy.make(JobCategory)
        )

        home = Page.objects.get(slug='home-page')
        home.add_child(instance=page)

        for grade in grades:
            grade_model = mommy.make(Grade, grade=grade)
            GradePanel.objects.create(grade=grade_model, job_listing=page)

        for region in regions:
            region_model = mommy.make(Location, region_long=region)
            RegionPanel.objects.create(region=region_model, job_listing=page)

    def assertHtmlRegexpMatches(self, s, r):
        s_no_right_spaces = re.sub('>\s*', '>', s)
        s_no_extra_spaces = re.sub('\s*<', '<', s_no_right_spaces)

        self.assertIsNotNone(
            re.search(r, s_no_extra_spaces.strip(), flags=re.DOTALL),
            '{} did not match {}'.format(s_no_extra_spaces, r)
        )
