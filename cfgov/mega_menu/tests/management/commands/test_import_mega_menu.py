import json
import uuid
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

import wagtail

from mega_menu.models import Menu


class ImportMegaMenuTests(TestCase):
    def test_no_menus_exist_by_default(self):
        self.assertFalse(Menu.objects.exists())

    def test_import(self):
        submenus = [
            {
                'type': 'submenu',
                'id': str(uuid.uuid4()),
                'value': {
                    'title': 'A submenu',
                    'overview_page': 123,
                    'links': [
                        {
                            'text': 'A link',
                            'url': '/foo/bar',
                        },
                    ],
                },
            }
        ]

        stdin = StringIO(json.dumps(submenus))
        stdout = StringIO()

        call_command('import_mega_menu', 'en', filename=stdin, stdout=stdout)
        self.assertEqual(
            stdout.getvalue(),
            'Created mega menu for language en.\n'
        )

        menu = Menu.objects.get(language='en')
        if wagtail.VERSION < (2, 12):  # pragma: no cover
            self.assertEqual(menu.submenus.stream_data, submenus)
        else:
            self.assertSequenceEqual(menu.submenus.raw_data, submenus)
