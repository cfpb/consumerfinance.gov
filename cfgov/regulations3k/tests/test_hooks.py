from __future__ import unicode_literals

from datetime import date

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from model_mommy import mommy

from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)
from regulations3k.models.pages import RegulationLandingPage, RegulationPage


class TestRegs3kHooks(TestCase, WagtailTestUtils):

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
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=date(2014, 1, 18),
            part=self.part_1002
        )
        self.subpart = mommy.make(
            Subpart,
            label='Subpart General',
            title='General',
            subpart_type=Subpart.BODY,
            version=self.effective_version
        )
        self.section_num4 = mommy.make(
            Section,
            label='4',
            title='\xa7\xa01002.4 General rules.',
            contents='{a}\n(a) Regdown paragraph a.\n',
            subpart=self.subpart,
        )

        self.login()

    def test_part_model_admin(self):
        response = self.client.get('/admin/regulations3k/part/')
        self.assertEqual(response.status_code, 200)

    def test_effectiveversion_model_admin(self):
        response = self.client.get('/admin/regulations3k/effectiveversion/')
        self.assertEqual(response.status_code, 200)

    def test_subpart_model_admin(self):
        response = self.client.get('/admin/regulations3k/subpart/')
        self.assertEqual(response.status_code, 200)

    def test_section_model_admin(self):
        response = self.client.get('/admin/regulations3k/section/')
        self.assertEqual(response.status_code, 200)

    def test_section_model_admin_no_preview_button(self):
        response = self.client.get('/admin/regulations3k/section/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Preview', response.content)

    def test_section_model_admin_has_preview_button(self):
        reg_page = RegulationPage(
            regulation=self.part_1002,
            title='Reg B',
            slug='1002')
        self.landing_page.add_child(instance=reg_page)
        reg_page.save()

        response = self.client.get('/admin/regulations3k/section/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Preview', response.content)
