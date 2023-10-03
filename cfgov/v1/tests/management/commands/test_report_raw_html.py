import json
import re
from io import StringIO
from unittest import TestCase

from django.core.management import call_command
from django.test import TestCase as DjangoTestCase

from wagtail.models import Site

from v1.management.commands.report_raw_html import find_pattern
from v1.models import BrowsePage


class FindPatternTestCase(TestCase):
    def setUp(self):
        self.pattern = re.compile(r"(dol\w+em)")
        self.str_data_matching = (
            "Neque porro quisquam est qui dolorem ipsum dolurem"
        )
        self.str_data_not_matching = (
            "quia dolor sit amet, consectetur, adipisci velit"
        )
        self.object_data_matching = {
            "id": "abcdefg0123456789",
            "type": "myblock",
            "value": self.str_data_matching,
        }
        self.object_data_not_matching = {
            "id": "abcdefg0123456789",
            "type": "myblock",
            "value": self.str_data_not_matching,
        }

    def test_string_matches_with_path(self):
        path_to_match = ["first"]
        path, matches = next(
            find_pattern(
                self.str_data_matching,
                self.pattern,
                "type",
                path=path_to_match,
            )
        )
        self.assertEqual(path, path_to_match)
        self.assertEqual(matches, ["dolorem", "dolurem"])

    def test_string_matches_without_path(self):
        path, matches = next(
            find_pattern(self.str_data_matching, self.pattern, "type")
        )
        self.assertEqual(path, [])

    def test_string_does_not_match(self):
        with self.assertRaises(StopIteration):
            next(
                find_pattern(self.str_data_not_matching, self.pattern, "type")
            )

    def test_object_with_key_and_path(self):
        path_to_match = ["first"]
        path, matches = next(
            find_pattern(
                self.object_data_matching,
                self.pattern,
                "type",
                path=path_to_match,
            )
        )
        self.assertEqual(path, path_to_match + ["myblock"])

    def test_object_without_key(self):
        with self.assertRaises(StopIteration):
            next(
                find_pattern(
                    self.object_data_not_matching, self.pattern, "type"
                )
            )

    def test_sequence_of_objects(self):
        path_to_match = ["first"]
        path, matches = next(
            find_pattern(
                [self.object_data_matching],
                self.pattern,
                "type",
                path=path_to_match,
            )
        )
        self.assertEqual(path, path_to_match + ["0", "myblock"])


class ReportRawHTMLTestCase(DjangoTestCase):
    def setUp(self):
        html_text = "<p>Some rich text&lt;br&gt;here.</p>"

        full_width_text = json.dumps(
            [
                {
                    "type": "full_width_text",
                    "value": [
                        {
                            "type": "content",
                            "value": html_text,
                        },
                    ],
                },
            ]
        )

        page = BrowsePage(title="test", slug="testpage")
        page.content = full_width_text

        site_root = Site.objects.get(is_default_site=True).root_page
        site_root.add_child(instance=page)

        page.save_revision().publish()

    def test_report_raw_html_with_page_type_and_field(self):
        output = StringIO()
        call_command("report_raw_html", "v1.BrowsePage.content", stdout=output)
        self.assertIn(
            "0.full_width_text.0.content",
            output.getvalue(),
        )

    def test_report_raw_html(self):
        output = StringIO()
        call_command("report_raw_html", stdout=output)
        self.assertIn(
            "0.full_width_text.0.content",
            output.getvalue(),
        )
