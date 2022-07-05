from unittest import mock

from django.apps import apps
from django.test import SimpleTestCase, TestCase

from wagtail.core import blocks
from wagtail.core.models import Page, Site
from wagtail.tests.testapp.models import StreamPage

from v1.models.snippets import EmailSignUp
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import (
    convert_emailsignup_block_to_snippet,
    get_streamfield_data,
    is_page,
    migrate_block,
    migrate_page_types_and_fields,
    migrate_stream_field,
    migrate_streamfield_data,
    set_streamfield_data,
)


class MigrationsUtilTestCase(TestCase):
    def setUp(self):
        self.root = Page.objects.get(slug="cfgov")
        self.page = StreamPage(title="Test Page", slug="testpage")
        save_new_page(self.page, self.root)
        set_streamfield_data(
            self.page, "body", [{"type": "text", "value": "some text"}]
        )

        self.revision = self.page.save_revision()
        self.page.save()

    def test_is_page_page(self):
        """Test that a page is verifably a page"""
        self.assertTrue(is_page(self.page))

    def test_is_page_revision(self):
        """Test that a revision is verifiably not a page"""
        self.assertFalse(is_page(self.revision))

    def test_get_streamfield_data_page(self):
        """Test that get_streamfield_data fetches the data correctly
        from a page object."""
        data = get_streamfield_data(self.page, "body")

        self.assertEqual(data[0]["type"], "text")
        self.assertEqual(data[0]["value"], "some text")

    def test_get_streamfield_data_revision(self):
        """Test that get_streamfield_data fetches the data correctly
        from a revision object."""
        data = get_streamfield_data(self.revision, "body")

        self.assertEqual(data[0]["type"], "text")
        self.assertEqual(data[0]["value"], "some text")

    def test_get_streamfield_data_revision_no_field(self):
        """Test that get an empty list for fields that don't exist on
        revisions"""
        data = get_streamfield_data(self.revision, "notbody")
        self.assertEqual(data, [])

    def test_set_streamfield_data_page(self):
        """Test that set_streamfield_data correctly sets data for a
        given page and saves the page."""
        new_data = [{"type": "text", "value": "new text"}]
        set_streamfield_data(self.page, "body", new_data)
        data = self.page.body.raw_data
        self.assertEqual(data[0]["value"], "new text")

    def test_set_streamfield_data_revision(self):
        """Test that set_streamfield_data correctly sets data for a
        given revision and saves the page."""
        new_data = [{"type": "text", "value": "new text"}]
        set_streamfield_data(self.revision, "body", new_data)
        data = self.revision.as_page_object().body.raw_data
        self.assertEqual(data[0]["value"], "new text")

    def test_set_streamfield_data_page_without_committing(self):
        """Test that set_streamfield_data correctly sets data for a
        given page and saves the page."""
        self.page.save = mock.Mock()

        new_data = [{"type": "text", "value": "new text"}]
        set_streamfield_data(self.page, "body", new_data, commit=False)

        self.assertEqual(self.page.save.mock_calls, [])

    def test_migrate_stream_field_page(self):
        """Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results."""
        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_streamfield_data.
        mapper = mock.Mock(return_value="new text")

        migrate_stream_field(self.page, "body", "text", mapper)

        mapper.assert_called_with(self.page, "some text")
        data = self.page.body.raw_data
        self.assertEqual(data[0]["value"], "new text")

    def test_migrate_stream_field_revision(self):
        """Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results."""
        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_streamfield_data.
        mapper = mock.Mock(return_value="new text")

        migrate_stream_field(self.revision, "body", "text", mapper)

        mapper.assert_called_with(self.revision, "some text")
        data = self.revision.as_page_object().body.raw_data
        self.assertEqual(data[0]["value"], "new text")

    @mock.patch("v1.util.migrations.set_streamfield_data")
    def test_migrate_stream_field_not_migrated(
        self, mock_set_streamfield_data
    ):
        """Test that the migrate_stream_field function correctly
        ignores a field that does not have the correct type and
        shouldn't be migrated."""
        mapper = mock.Mock()

        migrate_stream_field(self.page, "body", "other_type", mapper)

        # The mapper should not be called
        mapper.assert_not_called()

        # set_streamfield_data should not be called
        mock_set_streamfield_data.assert_not_called()

    @mock.patch("v1.util.migrations.migrate_stream_field")
    def test_migrate_page_types_and_fields(self, mock_migrate_stream_field):
        """Test that the migrate_page_types_and_fields function
        correctly calls the migrate_stream_field function with
        the appropriate values from the list of page types and
        fields."""
        mapper = mock.Mock()

        page_types_and_fields = [
            ("tests", "StreamPage", "body", "text"),
        ]
        migrate_page_types_and_fields(apps, page_types_and_fields, mapper)

        # Check that migrate_stream_field was correct called with the page
        mock_migrate_stream_field.assert_any_call(
            self.page, "body", "text", mapper
        )

        # Check that the revision lookup happened correctly and that the
        # revision stream field was correctly migrated.
        mock_migrate_stream_field.assert_any_call(
            self.revision, "body", "text", mapper
        )


class ChildStructBlock(blocks.StructBlock):
    text = blocks.CharBlock()


class ChildStreamBlock(blocks.StreamBlock):
    text = blocks.CharBlock()


class TestStreamBlock(blocks.StreamBlock):
    text = blocks.CharBlock()
    texts = blocks.ListBlock(blocks.CharBlock())
    struct = ChildStructBlock()
    stream = ChildStreamBlock()


class MigrateDataTests(SimpleTestCase):
    def setUp(self):
        self.page = "mock"

        self.original_data = [
            {"type": "text", "value": "foo"},
            {"type": "texts", "value": ["foo", "bar", "baz"]},
            {"type": "struct", "value": {"text": "bar"}},
            {
                "type": "stream",
                "value": [
                    {"type": "text", "value": "foo"},
                    {"type": "text", "value": "bar"},
                ],
            },
        ]

        self.block = TestStreamBlock()
        self.value = self.block.to_python(self.original_data)
        self.data = self.value.raw_data

    @staticmethod
    def mapper(page_or_revision, data):
        return "mapped"

    def test_migrate_data_empty_block_path(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "", self.data, self.mapper
        )
        self.assertFalse(migrated)
        self.assertSequenceEqual(modified_data, self.original_data)

    def test_migrate_data_invalid_block_path(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "invalid", self.data, self.mapper
        )
        self.assertFalse(migrated)
        self.assertSequenceEqual(modified_data, self.original_data)

    def test_migrate_data_raises_valueerror_on_bad_data(self):
        with self.assertRaises(ValueError):
            migrate_streamfield_data(
                self.page,
                ("parent", "child"),
                [{"type": "parent", "value": "invalid"}],
                self.mapper,
            )

    def test_migrate_data_top_level_block(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "text", self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "mapped"},
                {"type": "texts", "value": ["foo", "bar", "baz"]},
                {"type": "struct", "value": {"text": "bar"}},
                {
                    "type": "stream",
                    "value": [
                        {"type": "text", "value": "foo"},
                        {"type": "text", "value": "bar"},
                    ],
                },
            ],
        )

    def test_migrate_data_listblock(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "texts", self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "foo"},
                {"type": "texts", "value": ["mapped", "mapped", "mapped"]},
                {"type": "struct", "value": {"text": "bar"}},
                {
                    "type": "stream",
                    "value": [
                        {"type": "text", "value": "foo"},
                        {"type": "text", "value": "bar"},
                    ],
                },
            ],
        )

    def test_migrate_data_structblock(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "struct", self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "foo"},
                {"type": "texts", "value": ["foo", "bar", "baz"]},
                {"type": "struct", "value": "mapped"},
                {
                    "type": "stream",
                    "value": [
                        {"type": "text", "value": "foo"},
                        {"type": "text", "value": "bar"},
                    ],
                },
            ],
        )

    def test_migrate_data_structblock_child(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, ("struct", "text"), self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "foo"},
                {"type": "texts", "value": ["foo", "bar", "baz"]},
                {"type": "struct", "value": {"text": "mapped"}},
                {
                    "type": "stream",
                    "value": [
                        {"type": "text", "value": "foo"},
                        {"type": "text", "value": "bar"},
                    ],
                },
            ],
        )

    def test_migrate_data_streamblock(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, "stream", self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "foo"},
                {"type": "texts", "value": ["foo", "bar", "baz"]},
                {"type": "struct", "value": {"text": "bar"}},
                {"type": "stream", "value": "mapped"},
            ],
        )

    def test_migrate_data_streamblock_child(self):
        modified_data, migrated = migrate_streamfield_data(
            self.page, ("stream", "text"), self.data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertSequenceEqual(
            modified_data,
            [
                {"type": "text", "value": "foo"},
                {"type": "texts", "value": ["foo", "bar", "baz"]},
                {"type": "struct", "value": {"text": "bar"}},
                {
                    "type": "stream",
                    "value": [
                        {"type": "text", "value": "mapped"},
                        {"type": "text", "value": "mapped"},
                    ],
                },
            ],
        )

    def test_migrate_block_migrated_true_if_data_is_modified(self):
        def mapper_modifies_data(page_or_revision, data):
            data["b"] = "d"
            return data

        modified_data, migrated = migrate_block(
            self.page, ["a"], {"a": {"b": "c"}}, mapper_modifies_data
        )

        self.assertTrue(migrated)
        self.assertEqual(modified_data, {"a": {"b": "d"}})

    def test_migrate_block_migrated_false_if_data_is_modified(self):
        def mapper_leaves_data_alone(page_or_revision, data):
            return data

        modified_data, migrated = migrate_block(
            self.page, ["a"], {"a": {"b": "c"}}, mapper_leaves_data_alone
        )

        self.assertFalse(migrated)
        self.assertEqual(modified_data, {"a": {"b": "c"}})


class EmailSignupSnippetMigrationTestCase(TestCase):
    def setUp(self):
        root = Site.objects.get(is_default_site=True).root_page
        self.privacy_page = Page(title="Privacy Disclosure")
        root.add_child(instance=self.privacy_page)
        self.privacy_page.save()

    def test_creates_new_emailsignup_snippet_from_data(self):
        data = {
            "heading": "Stay informed",
            "default_heading": True,
            "text": "Sign up!",
            "gd_code": "USCFPB_1234",
            "disclaimer_page": self.privacy_page.pk,
        }

        # The migration should take the data, create a new EmailSignUp object,
        # and return the primary key of that new object.
        migrated_data = convert_emailsignup_block_to_snippet(apps, None, data)

        # Ensure we got an integer back
        self.assertIsInstance(migrated_data, int)

        # Get the new EmailSignUp object
        new_email_signup = EmailSignUp.objects.get(pk=migrated_data)

        # Check that it holds the same data as the old one
        self.assertEqual(new_email_signup.heading, data["heading"])
        self.assertEqual(
            new_email_signup.default_heading, data["default_heading"]
        )
        self.assertEqual(new_email_signup.text, data["text"])
        self.assertEqual(new_email_signup.code, data["gd_code"])
        self.assertEqual(new_email_signup.disclaimer_page, self.privacy_page)

    def test_uses_existing_email_signup_from_data(self):
        data = {
            "heading": "Stay informed",
            "default_heading": True,
            "text": "Sign up!",
            "gd_code": "USCFPB_1234",
            "disclaimer_page": self.privacy_page.pk,
        }

        # Create the snippet manually
        existing_emailsignup = EmailSignUp(
            topic=data["heading"],
            heading=data["heading"],
            default_heading=data["default_heading"],
            text=data["text"],
            code=data["gd_code"],
            disclaimer_page=Page.objects.get(pk=data["disclaimer_page"]),
        )
        existing_emailsignup.save()

        # The migration should take the data, find the existing EmailSignUp
        # object, and return the primary key of that existing object.
        migrated_data = convert_emailsignup_block_to_snippet(apps, None, data)

        # Ensure we got an integer back
        self.assertIsInstance(migrated_data, int)

        # Get the new EmailSignUp object
        migrated_emailsignup = EmailSignUp.objects.get(pk=migrated_data)

        # Check that the migrated one is the same as the existing one.
        self.assertEqual(migrated_emailsignup.pk, existing_emailsignup.pk)
