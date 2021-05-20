import datetime
from django.test import RequestFactory, TestCase, override_settings
from model_bakery import baker

from regulations3k.models import (
    EffectiveVersion, Part, RegulationLandingPage, RegulationPage, Section,
    Subpart
)


@override_settings(FLAGS={'REGULATIONS3K': [('boolean', True)]})
class PagesRegulations3kTestCase(TestCase):

    def setUp(self):
        from v1.models import HomePage
        self.factory = RequestFactory()
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

    def test_url_path(self):
        self.assertEqual(
            self.section_interp2.url_path, self.section_interp2.label.lower()
        )

    def test_redirect_uppercase(self):
        response = self.client.get(
            '/policy-compliance/rulemaking/regulations/1002/Interp-2/'
        )
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/interp-2/')
