from datetime import date

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from model_bakery import baker

from regulations3k.models.django import (
    EffectiveVersion,
    Part,
    Section,
    Subpart,
)
from regulations3k.models.pages import RegulationLandingPage, RegulationPage
from regulations3k.wagtail_hooks import RegsURLHelper


class TestRegs3kHooks(TestCase, WagtailTestUtils):
    def setUp(self):
        from v1.models import HomePage

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.landing_page = RegulationLandingPage(
            title="Reg Landing", slug="reg-landing"
        )
        self.ROOT_PAGE.add_child(instance=self.landing_page)

        self.part_1002 = baker.make(
            Part,
            part_number="1002",
            title="Equal Credit Opportunity Act",
            short_name="Regulation B",
            chapter="X",
        )
        self.effective_version = baker.make(
            EffectiveVersion,
            effective_date=date(2014, 1, 18),
            part=self.part_1002,
        )
        self.subpart = baker.make(
            Subpart,
            label="Subpart General",
            title="General",
            subpart_type=Subpart.BODY,
            version=self.effective_version,
        )
        self.section_num4 = baker.make(
            Section,
            label="4",
            title="\xa7\xa01002.4 General rules.",
            contents="{a}\n(a) Regdown paragraph a.\n",
            subpart=self.subpart,
        )

        self.draft_effective_version = baker.make(
            EffectiveVersion,
            effective_date=date(2020, 1, 18),
            part=self.part_1002,
            draft=True,
        )
        self.draft_subpart = baker.make(
            Subpart,
            label="Subpart General",
            title="General",
            subpart_type=Subpart.BODY,
            version=self.draft_effective_version,
        )
        self.draft_section_num4 = baker.make(
            Section,
            label="4",
            title="\xa7\xa01002.4 General rules.",
            contents="{a}\n(a) Regdown paragraph a.\n",
            subpart=self.draft_subpart,
        )

        self.login()

    def test_part_model_admin(self):
        response = self.client.get("/admin/regulations3k/part/")
        self.assertEqual(response.status_code, 200)

    def test_effectiveversion_model_admin(self):
        response = self.client.get("/admin/regulations3k/effectiveversion/")
        self.assertEqual(response.status_code, 200)

    def test_subpart_model_admin(self):
        response = self.client.get("/admin/regulations3k/subpart/")
        self.assertEqual(response.status_code, 200)

    def test_section_model_admin(self):
        response = self.client.get("/admin/regulations3k/section/")
        self.assertEqual(response.status_code, 200)

    def test_section_model_admin_no_preview_button(self):
        response = self.client.get("/admin/regulations3k/section/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"View live", response.content)
        self.assertNotIn(b"View draft", response.content)

    def test_section_model_admin_has_preview_button(self):
        reg_page = RegulationPage(
            regulation=self.part_1002, title="Reg B", slug="1002"
        )
        self.landing_page.add_child(instance=reg_page)
        reg_page.save()

        response = self.client.get("/admin/regulations3k/section/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"View live", response.content)
        self.assertIn(b"View draft", response.content)

    def test_regs_url_helper(self):
        helper = RegsURLHelper(Section)

        self.assertNotIn(
            self.subpart.__str__(),
            helper.crumb(
                parent_field="subpart",
                parent_instance=self.subpart,
                specific_instance=self.section_num4,
            )[1],
        )

        self.assertEqual(
            self.section_num4.__str__(),
            helper.crumb(
                specific_instance=self.section_num4,
            )[1],
        )
