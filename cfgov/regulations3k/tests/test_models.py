from __future__ import unicode_literals

import datetime
import sys

from django.http import HttpRequest  # Http404, HttpResponse
from django.test import TestCase as DjangoTestCase

from model_mommy import mommy
from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart, sortable_label
)
from regulations3k.models.pages import (
    RegulationLandingPage, RegulationPage, get_reg_nav_items
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
            label='1002',
            title='',
            version=self.effective_version
        )
        self.subpart_appendices = mommy.make(
            Subpart,
            label='1002-Appendices',
            title='APPENDICES',
            version=self.effective_version
        )
        self.section_num4 = mommy.make(
            Section,
            label='1002-4',
            title='\xa7 1002.4 General rules.',
            contents='regdown content.',
            subpart=self.subpart,
        )
        self.section_num15 = mommy.make(
            Section,
            label='1002-15',
            title='\xa7 1002.5 Rules concerning requests for information.',
            contents='regdown content.',
            subpart=self.subpart,
        )
        self.section_alpha = mommy.make(
            Section,
            label='1002-A',
            title=('Appendix A to Part 1002-Federal Agencies '
                   'To Be Listed in Adverse Action Notices'),
            contents='regdown content.',
            subpart=self.subpart_appendices,
        )
        self.reg_page = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='reg-b')

        self.landing_page.add_child(instance=self.reg_page)

    def test_part_string_method(self):
        self.assertEqual(
            self.part_1002.__str__(),
            '12 CFR Part 1002 (Regulation B)'
        )

    def test_subpart_string_method(self):
        self.assertEqual(
            self.subpart.__str__(),
            '1002 , effective 2014-01-18')

    def test_section_string_method(self):
        if sys.version_info >= (3, 0):
            self.assertEqual(
                self.section_num4.__str__(),
                '1002-4 \xa7 1002.4 General rules.')
        else:
            self.assertEqual(
                self.section_num4.__str__(),
                '1002-4 \xa7 1002.4 General rules.'.encode('utf8'))

    def test_effective_version_string_method(self):
        self.assertEqual(
            self.effective_version.__str__(),
            '12 CFR Part 1002 (Regulation B), effective 2014-01-18')

    def test_landing_page_get_context(self):
        test_context = self.landing_page.get_context(HttpRequest())
        self.assertIn(self.part_1002, test_context['regs'])

    def test_landing_page_get_template(self):
        self.assertEqual(
            self.landing_page.get_template(HttpRequest()),
            'regulations3k/base.html')

    def test_routable_page_get_context(self):
        test_context = self.reg_page.get_context(HttpRequest())
        self.assertEqual(
            test_context['regulation'],
            self.reg_page.regulation)

    def test_get_reg_nav_items(self):
        request = HttpRequest()
        request.url = '/eregulations3k/1002/1002-4/'
        test_nav_items = get_reg_nav_items(request, self.reg_page)[0]
        self.assertEqual(
            len(test_nav_items),
            Section.objects.filter(
                label__startswith='1002').count())

    def test_routable_page_view(self):
        response = self.reg_page.section_page(
            HttpRequest(), section='4')
        self.assertEqual(response.status_code, 200)

    def test_sortable_label(self):
        self.assertEqual(sortable_label('1-A-Interp'), ('0001', 'A', 'interp'))

    def test_sorted_sections(self):
        sorted_sections = [s.label for s in self.reg_page.sorted_sections]
        self.assertEqual(sorted_sections, ['1002-4', '1002-15', '1002-A'])

    def test_render_interp(self):
        result = self.reg_page.render_interp({}, 'some contents')
        self.assertIn('some contents', result)
