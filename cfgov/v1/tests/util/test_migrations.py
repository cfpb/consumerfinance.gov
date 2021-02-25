# -*- coding: utf-8 -*-
from unittest import mock

from django.apps import apps
from django.test import SimpleTestCase, TestCase

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.tests.testapp.models import StreamPage

from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import (
    get_stream_data, is_page, migrate_page_types_and_fields,
    migrate_stream_data, migrate_stream_field, set_stream_data
)


class MigrationsUtilTestCase(TestCase):

    def setUp(self):
        self.root = Page.objects.get(slug='cfgov')
        self.page = StreamPage(title="Test Page", slug="testpage")
        save_new_page(self.page, self.root)
        set_stream_data(self.page, 'body', [
            {'type': 'text', 'value': 'some text'}
        ])

        self.revision = self.page.save_revision()
        self.page.save()

    def test_is_page_page(self):
        """ Test that a page is verifably a page """
        self.assertTrue(is_page(self.page))

    def test_is_page_revision(self):
        """ Test that a revision is verifiably not a page """
        self.assertFalse(is_page(self.revision))

    def test_get_stream_data_page(self):
        """ Test that get_stream_data fetches the stream_data correctly
        from a page object. """
        stream_data = get_stream_data(self.page, 'body')

        self.assertEqual(stream_data[0]['type'], 'text')
        self.assertEqual(stream_data[0]['value'], 'some text')

    def test_get_stream_data_revision(self):
        """ Test that get_stream_data fetches the stream_data correctly
        from a revision object. """
        stream_data = get_stream_data(self.revision, 'body')

        self.assertEqual(stream_data[0]['type'], 'text')
        self.assertEqual(stream_data[0]['value'], 'some text')

    def test_get_stream_data_revision_no_field(self):
        """ Test that get an empty list for fields that don't exist on
        revisions """
        stream_data = get_stream_data(self.revision, 'notbody')
        self.assertEqual(stream_data, [])

    def test_set_stream_data_page(self):
        """ Test that set_stream_data correctly sets stream data for a
        given page and saves the page. """
        new_stream_data = [{'type': 'text', 'value': 'new text'}]
        set_stream_data(self.page, 'body', new_stream_data)

        self.assertEqual(self.page.body.stream_data[0]['value'], 'new text')

    def test_set_stream_data_revision(self):
        """ Test that set_stream_data correctly sets stream data for a
        given revision and saves the page. """
        new_stream_data = [{'type': 'text', 'value': 'new text'}]
        set_stream_data(self.revision, 'body', new_stream_data)

        self.assertEqual(
            self.revision.as_page_object().body.stream_data[0]['value'],
            'new text')

    def test_set_stream_data_page_without_committing(self):
        """ Test that set_stream_data correctly sets stream data for a
        given page and saves the page. """
        self.page.save = mock.Mock()

        new_stream_data = [{'type': 'text', 'value': 'new text'}]
        set_stream_data(self.page, 'body', new_stream_data, commit=False)

        self.assertEqual(self.page.save.mock_calls, [])

    def test_migrate_stream_field_page(self):
        """ Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results. """
        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_stream_data.
        mapper = mock.Mock(return_value='new text')

        migrate_stream_field(self.page, 'body', 'text', mapper)

        mapper.assert_called_with(self.page, 'some text')
        self.assertEqual(self.page.body.stream_data[0]['value'],
                         'new text')

    def test_migrate_stream_field_revision(self):
        """ Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results. """
        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_stream_data.
        mapper = mock.Mock(return_value='new text')

        migrate_stream_field(self.revision, 'body', 'text', mapper)

        mapper.assert_called_with(self.revision, 'some text')
        self.assertEqual(
            self.revision.as_page_object().body.stream_data[0]['value'],
            'new text')

    @mock.patch('v1.util.migrations.set_stream_data')
    def test_migrate_stream_field_not_migrated(self,
                                               mock_set_stream_data):
        """ Test that the migrate_stream_field function correctly
        ignores a field that does not have the correct type and
        shouldn't be migrated. """
        mapper = mock.Mock()

        migrate_stream_field(self.page, 'body', 'other_type', mapper)

        # The mapper should not be called
        mapper.assert_not_called()

        # set_stream_data should not be called
        mock_set_stream_data.assert_not_called()

    @mock.patch('v1.util.migrations.migrate_stream_field')
    def test_migrate_page_types_and_fields(self,
                                           mock_migrate_stream_field):
        """ Test that the migrate_page_types_and_fields function
        correctly calls the migrate_stream_field function with
        the appropriate values from the list of page types and
        fields. """
        mapper = mock.Mock()

        page_types_and_fields = [
            ('tests', 'StreamPage', 'body', 'text'),
        ]
        migrate_page_types_and_fields(apps, page_types_and_fields, mapper)

        # Check that migrate_stream_field was correct called with the page
        mock_migrate_stream_field.assert_any_call(self.page,
                                                  'body',
                                                  'text',
                                                  mapper)

        # Check that the revision lookup happened correctly and that the
        # revision stream field was correctly migrated.
        mock_migrate_stream_field.assert_any_call(self.revision,
                                                  'body',
                                                  'text',
                                                  mapper)


class ChildStructBlock(blocks.StructBlock):
    text = blocks.CharBlock()

class ChildStreamBlock(blocks.StreamBlock):
    text = blocks.CharBlock()

class TestStreamBlock(blocks.StreamBlock):
    text = blocks.CharBlock()
    texts = blocks.ListBlock(blocks.CharBlock())
    struct = ChildStructBlock()
    stream = ChildStreamBlock()


class MigrateStreamDataTests(SimpleTestCase):
    def setUp(self):
        self.page = 'mock'

        self.original_stream_data = [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': {'text': 'bar'}},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]},
        ]

        self.block = TestStreamBlock()
        self.value = self.block.to_python(self.original_stream_data)

    @staticmethod
    def mapper(page_or_revision, data):
        return 'mapped'

    def test_migrate_stream_data_empty_block_path(self):
        modified_data, migrated = migrate_stream_data(
            self.page, '', self.value.stream_data, self.mapper
        )
        self.assertFalse(migrated)
        self.assertEqual(modified_data, self.original_stream_data)

    def test_migrate_stream_data_invalid_block_path(self):
        modified_data, migrated = migrate_stream_data(
            self.page, 'invalid', self.value.stream_data, self.mapper
        )
        self.assertFalse(migrated)
        self.assertEqual(modified_data, self.original_stream_data)

    def test_migrate_stream_data_raises_valueerror_on_bad_data(self):
        with self.assertRaises(ValueError):
            migrate_stream_data(
                self.page,
                ('parent', 'child'),
                [{'type': 'parent', 'value': 'invalid'}],
                self.mapper
            )

    def test_migrate_stream_data_top_level_block(self):
        modified_data, migrated = migrate_stream_data(
            self.page, 'text', self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'mapped'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': {'text': 'bar'}},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]},
        ])

    def test_migrate_stream_data_listblock(self):
        modified_data, migrated = migrate_stream_data(
            self.page, 'texts', self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['mapped', 'mapped', 'mapped']},
            {'type': 'struct', 'value': {'text': 'bar'}},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]},
        ])

    def test_migrate_stream_data_structblock(self):
        modified_data, migrated = migrate_stream_data(
            self.page, 'struct', self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': 'mapped'},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]},
        ])

    def test_migrate_stream_data_structblock_child(self):
        modified_data, migrated = migrate_stream_data(
            self.page, ('struct', 'text'), self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': {'text': 'mapped'}},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]},
        ])

    def test_migrate_stream_data_streamblock(self):
        modified_data, migrated = migrate_stream_data(
            self.page, 'stream', self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': {'text': 'bar'}},
            {'type': 'stream', 'value': 'mapped'},
        ])

    def test_migrate_stream_data_streamblock_child(self):
        modified_data, migrated = migrate_stream_data(
            self.page, ('stream', 'text'), self.value.stream_data, self.mapper
        )
        self.assertTrue(migrated)
        self.assertEqual(modified_data, [
            {'type': 'text', 'value': 'foo'},
            {'type': 'texts', 'value': ['foo', 'bar', 'baz']},
            {'type': 'struct', 'value': {'text': 'bar'}},
            {'type': 'stream', 'value': [
                {'type': 'text', 'value': 'mapped'},
                {'type': 'text', 'value': 'mapped'},
            ]},
        ])
