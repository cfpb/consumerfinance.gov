from __future__ import unicode_literals

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils


class TestRegs3kHooks(TestCase, WagtailTestUtils):

    def setUp(self):
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
