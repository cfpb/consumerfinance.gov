from datetime import date

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from model_bakery import baker

from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)


class TestCopyableModelAdmin(TestCase, WagtailTestUtils):

    def setUp(self):
        self.part_1002 = baker.make(
            Part,
            part_number='1002',
            title='Equal Credit Opportunity Act',
            short_name='Regulation B',
            chapter='X'
        )
        self.effective_version = baker.make(
            EffectiveVersion,
            effective_date=date(2014, 1, 18),
            part=self.part_1002
        )
        self.subpart = baker.make(
            Subpart,
            label='Subpart General',
            title='General',
            subpart_type=Subpart.BODY,
            version=self.effective_version
        )
        self.section_num4 = baker.make(
            Section,
            label='4',
            title='\xa7\xa01002.4 General rules.',
            contents='{a}\n(a) Regdown paragraph a.\n',
            subpart=self.subpart,
        )

        self.login()

    def test_effectiveversion_copyable(self):
        response = self.client.get('/admin/regulations3k/effectiveversion/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Copy this effective version')

    def test_copy_effectiveversion(self):
        self.assertEqual(EffectiveVersion.objects.count(), 1)
        self.assertEqual(Subpart.objects.count(), 1)
        self.assertEqual(Section.objects.count(), 1)

        num_versions = EffectiveVersion.objects.count()

        existing_url = (
            '/admin/regulations3k/effectiveversion/copy/' +
            str(self.effective_version.pk) +
            '/'
        )
        response = self.client.get(existing_url)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(EffectiveVersion.objects.count(), num_versions + 1)
        new_effective_version = EffectiveVersion.objects.all().order_by(
            '-id'
        ).first()

        self.assertEqual(new_effective_version.subparts.count(), 1)
        new_subpart = new_effective_version.subparts.first()
        self.assertEqual(new_subpart.version, new_effective_version)
        self.assertNotEqual(self.subpart, new_subpart)

        self.assertEqual(new_subpart.sections.count(), 1)
        new_section = new_subpart.sections.first()
        self.assertEqual(new_section.subpart, new_subpart)
        self.assertNotEqual(self.section_num4, new_section)

        self.assertEqual(self.effective_version.subparts.count(), 1)
        self.assertEqual(self.subpart.sections.count(), 1)
