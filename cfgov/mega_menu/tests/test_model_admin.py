import json

from django.test import TestCase, override_settings

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
                                    'link': {
                                        'url': '/foo/bar/',
                                        'text': 'Test menu link',
                                    },
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

    def test_edit_view_contains_preview_button(self):
        response = self.client.get('/admin/mega_menu/menu/edit/en/')
        self.assertContains(response, 'Preview')

    @override_settings(FLAGS={'MEGA_MENU_BACKEND_V2': [('boolean', True)]})
    def test_preview_view(self):
        response = self.client.get('/admin/mega_menu/menu/preview/en/')
        self.assertContains(response, 'Test column heading')
