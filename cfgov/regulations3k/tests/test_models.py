from __future__ import unicode_literals

import datetime
import sys
import unittest

# from django.core.urlresolvers import reverse
from django.http import HttpRequest  # Http404, HttpResponse
from django.test import TestCase as DjangoTestCase

import mock
from model_mommy import mommy

from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart, sortable_label
)
from regulations3k.models.pages import (
    RegulationLandingPage, RegulationPage, RegulationsSearchPage,
    get_next_section, get_previous_section, get_reg_nav_items
)


class RegModelTests(DjangoTestCase):
    def setUp(self):
        from v1.models import HomePage
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.landing_page = RegulationLandingPage(
            title='Reg Landing', slug='reg-landing')
        self.ROOT_PAGE.add_child(instance=self.landing_page)

        self.part_1002 = mommy.make(
            Part,
            part_number='1002',
            title='Equal Credit Opportunity Act',
            letter_code='B',
            chapter='X'
        )
        self.part_1030 = mommy.make(
            Part,
            part_number='1030',
            title='Truth In Savings',
            letter_code='DD', chapter='X'
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002
        )
        self.subpart = mommy.make(
            Subpart,
            label='Subpart-General',
            title='General',
            subpart_type=Subpart.BODY,
            version=self.effective_version
        )
        self.subpart_appendices = mommy.make(
            Subpart,
            label='Appendices',
            title='Appendices',
            subpart_type=Subpart.APPENDIX,
            version=self.effective_version
        )
        self.subpart_interps = mommy.make(
            Subpart,
            label='Official-Interpretations',
            title='Supplement I to Part 1002',
            subpart_type=Subpart.INTERPRETATION,
            version=self.effective_version
        )
        self.subpart_orphan = mommy.make(
            Subpart,
            label='General-Mistake',
            title='An orphan subpart with no sections for testing',
            version=self.effective_version
        )
        self.section_num4 = mommy.make(
            Section,
            label='4',
            title='\xa7\xa01002.4 General rules.',
            contents='regdown content.',
            subpart=self.subpart,
        )
        self.section_num15 = mommy.make(
            Section,
            label='15',
            title='\xa7\xa01002.15 Rules concerning requests for information.',
            contents='regdown content.',
            subpart=self.subpart,
        )
        self.section_alpha = mommy.make(
            Section,
            label='A',
            title=('Appendix A to Part 1002-Federal Agencies '
                   'To Be Listed in Adverse Action Notices'),
            contents='regdown content.',
            subpart=self.subpart_appendices,
        )
        self.section_beta = mommy.make(
            Section,
            label='B',
            title=('Appendix B to Part 1002-Errata'),
            contents='regdown content.',
            subpart=self.subpart_appendices,
        )
        self.section_interps = mommy.make(
            Section,
            label='Interp-A',
            title=('Official interpretations for Appendix A to Part 1002'),
            contents='interp content.',
            subpart=self.subpart_interps,
        )
        self.reg_page = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='1002')

        self.reg_search_page = RegulationsSearchPage(
            title="Regulation search",
            slug='reg-search')

        self.landing_page.add_child(instance=self.reg_page)
        self.landing_page.add_child(instance=self.reg_search_page)
        self.reg_search_page.save()

    def test_part_string_method(self):
        self.assertEqual(
            self.part_1002.__str__(),
            '12 CFR Part 1002 (Regulation B)'
        )

    def test_part_cfr_title_method(self):
        part = self.part_1002
        self.assertEqual(
            part.cfr_title,
            "{} CFR Part {} (Regulation {})".format(
                part.cfr_title_number,
                part.part_number,
                part.letter_code))

    def test_subpart_string_method(self):
        self.assertEqual(
            self.subpart.__str__(),
            'General')

    def test_section_string_method(self):
        if sys.version_info >= (3, 0):
            self.assertEqual(
                self.section_num4.__str__(),
                '\xa7\xa01002.4 General rules.')
        else:
            self.assertEqual(
                self.section_num4.__str__(),
                '\xa7\xa01002.4 General rules.'.encode('utf8'))

    def test_subpart_headings(self):
        for each in Subpart.objects.all():
            self.assertEqual(each.subpart_heading, '')

    def test_effective_version_string_method(self):
        self.assertEqual(
            self.effective_version.__str__(),
            'Effective on 2014-01-18')

    def test_landing_page_get_context(self):
        test_context = self.landing_page.get_context(HttpRequest())
        self.assertIn(self.part_1002, test_context['regs'])

    def test_landing_page_get_template(self):
        self.assertEqual(
            self.landing_page.get_template(HttpRequest()),
            'regulations3k/base.html')

    def test_search_page_get_template(self):
        self.assertEqual(
            self.reg_search_page.get_template(HttpRequest()),
            'regulations3k/search-regulations.html')

    def test_routable_reg_page_get_context(self):
        test_context = self.reg_page.get_context(HttpRequest())
        self.assertEqual(
            test_context['regulation'],
            self.reg_page.regulation)

    def test_get_reg_nav_items(self):
        request = HttpRequest()
        request.url = '/regulations/1002/4/'
        test_nav_items = get_reg_nav_items(request, self.reg_page)[0]
        self.assertEqual(
            len(test_nav_items),
            Subpart.objects.filter(
                version__part__part_number='1002').exclude(
                sections=None).count())

    def test_routable_page_view(self):
        response = self.reg_page.section_page(
            HttpRequest(), section_label='4')
        self.assertEqual(response.status_code, 200)

    def test_sortable_label(self):
        self.assertEqual(sortable_label('1-A-Interp'), ('0001', 'A', 'interp'))

    def test_sections(self):
        sections = [s.label for s in self.reg_page.sections]
        self.assertEqual(
            sections,
            ['4', '15', 'A', 'B', 'Interp-A']
        )

    def test_render_interp(self):
        result = self.reg_page.render_interp({}, 'some contents')
        self.assertIn('some contents', result)

    def test_render_interp_with_title(self):
        result = self.reg_page.render_interp(
            {},
            '# A title\n\nsome contents'
        )
        self.assertIn('Official interpretation of A title', result)
        self.assertIn('some contents', result)

    def test_section_ranges(self):
        self.assertEqual(self.subpart_orphan.section_range, '')
        self.assertEqual(self.subpart_appendices.section_range, '')
        self.assertEqual(self.subpart_interps.section_range, '')
        self.assertEqual(
            self.subpart.section_range,
            '\xa7\xa01002.4\u2013\xa7\xa01002.15')

    def test_section_title_content(self):
        self.assertEqual(
            self.section_num15.title_content,
            'Rules concerning requests for information.')

    def test_section_part(self):
        self.assertEqual(self.section_num4.part, '1002')

    def test_section_section_number(self):
        self.assertEqual(self.section_num4.section_number, '4')

    def test_section_numeric_label(self):
        self.assertEqual(self.section_num4.numeric_label, '\xa7\xa01002.4')

    def test_section_numeric_label_not_digits(self):
        self.assertEqual(self.section_alpha.numeric_label, '')

    def test_section_title_content_not_digits(self):
        self.assertEqual(
            self.section_beta.title_content,
            'Appendix B to Part 1002-Errata'
        )

    @mock.patch('regulations3k.models.pages.SearchQuerySet')
    def test_routable_search_page_calls_elasticsearch(self, mock_ES):
        mock_return = mock.Mock()
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_sqs_instance = mock_ES()
        mock_sqs_instance.filter.return_value.models.return_value = (
            mock_queryset)
        response = self.client.get(self.reg_search_page.reverse_subpage(
            'regulation_results_page'),
            {'q': 'disclosure', 'regs': '1002,1003'})
        self.assertEqual(mock_ES.call_count, 1)
        self.assertEqual(response.status_code, 404)


class SectionNavTests(unittest.TestCase):

    def test_get_next_section(self):
        section_list = ['1002.1', '1002.2']
        current_index = 0
        self.assertEqual(
            get_next_section(section_list, current_index), '1002.2')

    def test_get_next_section_none(self):
        section_list = ['1002.1', '1002.2']
        current_index = 1
        self.assertIs(
            get_next_section(section_list, current_index), None)

    def test_get_previous_section(self):
        section_list = ['1002.1', '1002.2']
        current_index = 1
        self.assertEqual(
            get_previous_section(section_list, current_index), '1002.1')

    def test_get_previous_section_none(self):
        section_list = ['1002.1', '1002.2']
        current_index = 0
        self.assertIs(
            get_previous_section(section_list, current_index), None)
