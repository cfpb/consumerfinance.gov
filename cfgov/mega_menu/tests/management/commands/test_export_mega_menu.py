import json
import uuid
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from mega_menu.models import Menu


class ExportMegaMenuTests(TestCase):
    def test_export(self):
        submenus = [
            {
                "id": str(uuid.uuid4()),
                "type": "submenu",
                "value": {
                    "links": [
                        {"url": "/foo/bar", "text": "A link"},
                    ],
                    "title": "A submenu",
                    "overview_page": 123,
                },
            }
        ]

        Menu.objects.create(language="en", submenus=json.dumps(submenus))

        stdout = StringIO()
        call_command("export_mega_menu", "en", filename=stdout)

        self.assertEqual(stdout.getvalue(), json.dumps(submenus, indent=4))
