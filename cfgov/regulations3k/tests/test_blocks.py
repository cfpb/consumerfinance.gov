from __future__ import unicode_literals

import datetime

from django.test import TestCase, override_settings

from wagtail.wagtailcore.blocks import StreamValue
from wagtail.wagtailcore.models import Page

from model_mommy import mommy

from regulations3k.blocks import NotificationBlock, RegulationsList
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
        self.part_1003 = mommy.make(
            Part,
            part_number='1003',
            title='Home Mortgage Disclosure',
            letter_code='C',
            chapter='X'
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002
        )
        self.reg_page_1002 = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='1002'
        )
        self.reg_page_1003 = RegulationPage(
            regulation=self.part_1003,
            title='Reg C',
            slug='1003',
            live=False,
        )

        self.landing_page.add_child(instance=self.reg_page_1002)
        self.landing_page.add_child(instance=self.reg_page_1003)
        self.landing_page.save_revision().publish()
        self.reg_page_1002.save_revision().publish()
        self.reg_page_1003.save_revision()

        self.more_regs_page = Page.objects.first()

    def test_regulations_list_has_regs(self):
        block = RegulationsList()
        result = block.render(block.to_python({
            'more_regs_page': self.more_regs_page.pk,
        }))
        self.assertIn('Reg B', result)
        self.assertIn('/regulations/1002/', result)
        self.assertNotIn('Reg C', result)
        self.assertNotIn('/regulations/1003/', result)

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
                            'citation': 'a citation',
                            'more_regs_page': self.more_regs_page.pk,
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


class NotificationBlockTestCase(TestCase):

    def test_notification_block(self):
        block = NotificationBlock()
        result = block.render(block.to_python({
            'message': 'Test notification',
            'explanation': 'For testing',
            'notification_type': 'warning',
        }))
        self.assertIn('m-notification__warning', result)
        self.assertIn(
            '<div class="h4 m-notification_message">Test notification</div>',
            result
        )
        self.assertIn(
            '<p class="m-notification_explanation">For testing</p>',
            result
        )

    def test_notification_block_without_explanation(self):
        block = NotificationBlock()
        result = block.render(block.to_python({
            'message': 'Test notification',
            'notification_type': 'warning',
        }))
        self.assertNotIn('m-notification_explanation', result)

    def test_notification_block_success(self):
        block = NotificationBlock()
        result = block.render(block.to_python({
            'message': 'Test notification',
            'explanation': 'For testing',
            'notification_type': 'success',
        }))
        self.assertIn('cf-icon-svg', result)
