from __future__ import unicode_literals

import datetime

from django.test import Client, TestCase, override_settings

from wagtail.wagtailcore.blocks import StreamValue

from model_mommy import mommy

from regulations3k.blocks import RegulationsList
from regulations3k.models.django import EffectiveVersion, Part
from regulations3k.models.pages import RegulationLandingPage, RegulationPage


@override_settings(
    FLAGS={'REGULATIONS3K': {'boolean': True}}
)
class RegulationsListTestCase(TestCase):

    def setUp(self):
        from v1.models import HomePage
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.landing_page = RegulationLandingPage(
            title='Reg Landing',
            slug='regulations'
        )
        self.ROOT_PAGE.add_child(instance=self.landing_page)

        self.part_1002 = mommy.make(
            Part,
            part_number='1002',
            title='Equal Credit Opportunity Act',
            letter_code='B',
            chapter='X'
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002
        )
        self.reg_page = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='1002')

        self.landing_page.add_child(instance=self.reg_page)
        self.landing_page.save_revision().publish()
        self.reg_page.save_revision().publish()

        self.client = Client()

    def test_regulations_list_has_regs(self):
        block = RegulationsList()
        result = block.render(block.to_python({}))
        self.assertIn('Reg B', result)
        self.assertIn('/regulations/1002/', result)

    def test_regulations_full_width_text(self):
        self.landing_page.content = StreamValue(
            self.landing_page.content.stream_block,
            [{
                'type': 'full_width_text',
                'value': [
                    {
                        'type': 'content',
                        'value': 'Full width text content'
                    },
                    {
                        'type': 'regulations_list',
                        'value': {
                            'body': 'this is a quote',
                            'citation': 'a citation'
                        }
                    },
                ]
            }],
            True
        )
        self.landing_page.save_revision().publish()
        response = self.client.get('/regulations/')
        self.assertContains(response, 'Full width text content')
        self.assertContains(response, 'Reg B')
