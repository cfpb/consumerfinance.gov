# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase, override_settings

from model_bakery import baker
from regdown import DEFAULT_RENDER_BLOCK_REFERENCE, regdown

from regulations3k.models import (
    EffectiveVersion, Part, RegulationLandingPage, RegulationPage, Section,
    Subpart
)
from regulations3k.resolver import (
    get_contents_resolver, get_url_resolver, resolve_reference
)


# Our setup and tests use as close to regulation examples as possible.
# Override the default settings to let us map old-eRegs-style labels to new
# Regulations3k sections and paragraphs.
@override_settings(
    REGULATIONS_REFERENCE_MAPPING=[
        (
            r'(?P<label>(?P<section>[\w]+))-(?P<paragraph>[\w-]*-Interp)',
            'Interp-{section}',
            '{paragraph}'
        )
    ]
)
class ReferenceResolutionTestCase(TestCase):

    def setUp(self):
        from v1.models import HomePage
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.landing_page = RegulationLandingPage(
            title='Reg Landing', slug='reg-landing')
        self.ROOT_PAGE.add_child(instance=self.landing_page)

        self.part_1002 = baker.make(
            Part,
            part_number='1002',
            title='Equal Credit Opportunity Act',
            short_name='Regulation B',
            chapter='X'
        )
        self.effective_version = baker.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002
        )
        self.subpart = baker.make(
            Subpart,
            label='1002',
            title='',
            version=self.effective_version
        )
        self.subpart_interps = baker.make(
            Subpart,
            label='Interp',
            title='Suppliment I to Part 1002',
            version=self.effective_version
        )
        self.section_2 = baker.make(
            Section,
            label='2',
            title='\xa7 1002.2 Definitions.',
            contents='{c}\nAdverse action.\n\nsee(2-c-Interp)\n',
            subpart=self.subpart,
        )
        self.section_3 = baker.make(
            Section,
            label='3',
            title='\xa7 1002.3 Limited exceptions.',
            contents='{b}\nSecurities credit.\n\nsee(3-b-Interp)\n',
            subpart=self.subpart,
        )
        self.section_interp2 = baker.make(
            Section,
            label='Interp-2',
            title='Section 1002.2—Definitions',
            contents='{c-Interp}\nInterpreting adverse action\n\n',
            subpart=self.subpart,
        )

        self.reg_page = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='1002')
        self.landing_page.add_child(instance=self.reg_page)

    def test_resolve_reference(self):
        section, paragraph = resolve_reference('2-c-Interp')
        self.assertEqual(section, 'Interp-2')
        self.assertEqual(paragraph, 'c-Interp')

    def test_resolve_reference_no_match(self):
        section, paragraph = resolve_reference('foo')
        self.assertIsNone(section)
        self.assertIsNone(paragraph)

    def test_get_contents_resolver(self):
        contents_resolver = get_contents_resolver(
            self.reg_page.regulation.effective_version
        )
        result = regdown(
            self.section_2.contents,
            contents_resolver=contents_resolver,
            render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE
        )
        self.assertIn('Interpreting adverse action', result)

    def test_get_contents_resolver_reference_doesnt_exist(self):
        contents_resolver = get_contents_resolver(
            self.reg_page.regulation.effective_version
        )
        result = regdown(
            self.section_3.contents,
            contents_resolver=contents_resolver,
            render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE
        )
        self.assertEqual(
            result,
            '<p class="regdown-block level-0" data-label="b" id="b">'
            'Securities credit.</p>'
        )

    def test_get_url_resolver(self):
        url_resolver = get_url_resolver(self.reg_page)
        result = url_resolver('2-c-Interp')
        self.assertEqual(result, '/reg-landing/1002/interp-2/#c-Interp')
