from io import StringIO

from django.core.management import CommandError, call_command

from wagtail.models import Page

from core.testutils.test_cases import WagtailPageTreeTestCase
from v1.models import LearnPage, SublandingPage


class TestDeletePageCommand(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                SublandingPage(title="parent"),
                [
                    LearnPage(title="child1"),
                    LearnPage(title="child2"),
                ],
            )
        ]

    def test_must_provide_slug_or_id(self):
        with self.assertRaises(CommandError):
            call_command("delete_page", stdout=StringIO())

    def test_must_provide_only_slug_or_id(self):
        with self.assertRaises(CommandError):
            call_command(
                "delete_page",
                id=self.page_tree[0].pk,
                slug="parent",
                stdout=StringIO(),
            )

    def test_delete_by_id(self):
        count = Page.objects.count()
        call_command("delete_page", id=self.page_tree[0].pk, stdout=StringIO())
        self.assertEqual(Page.objects.count(), count - 3)

    def test_delete_by_slug(self):
        count = Page.objects.count()
        call_command("delete_page", slug="parent", stdout=StringIO())
        self.assertEqual(Page.objects.count(), count - 3)

    def test_dry_run(self):
        count = Page.objects.count()
        call_command(
            "delete_page", slug="parent", dry_run=True, stdout=StringIO()
        )
        self.assertEqual(Page.objects.count(), count)

    def test_children_only(self):
        count = Page.objects.count()
        call_command(
            "delete_page",
            id=self.page_tree[0].pk,
            children_only=True,
            stdout=StringIO(),
        )
        self.assertEqual(Page.objects.count(), count - 2)
