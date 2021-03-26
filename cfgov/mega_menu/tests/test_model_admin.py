import json

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from mega_menu.models import Menu


class ModelAdminTests(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    @classmethod
    def setUpTestData(cls):
        Menu.objects.create(language='en', submenus=json.dumps([
            {
                'type': 'submenu',
                'value': {
                    'columns': [
                        {
                            'heading': 'Test column heading',
                            'links': [
                                {
                                    'url': '/foo/bar/',
                                    'text': 'Test menu link',
                                },
                            ],
                        },
                    ],
                },
            },
        ]))

    def test_index_view_contains_preview_button(self):
        response = self.client.get('/admin/mega_menu/menu/')
        self.assertContains(response, 'Preview this menu')

    def test_preview_view(self):
        response = self.client.get('/admin/mega_menu/menu/preview/en/')
        self.assertContains(response, 'Test column heading')
