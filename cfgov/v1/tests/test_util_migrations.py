# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mock
from unittest import TestCase

from v1.util.migrations import (
    migrate_page_types_and_fields,
    migrate_stream_field,
    get_stream_data,
    set_stream_data,
)


class MigrationsUtilTestCase(TestCase):

    def test_get_stream_data_page(self):
        """ Test that get_stream_data fetches the stream_data correctly
        from a page object. """
        mock_field = mock.Mock()
        mock_field.stream_data = [{'type': 'test_field', 'value': 'testvalue'}]

        mock_page = mock.Mock()
        mock_page.my_field = mock_field

        stream_data = get_stream_data(mock_page, 'my_field')

        self.assertEqual(stream_data[0]['type'], 'test_field')
        self.assertEqual(stream_data[0]['value'], 'testvalue')

    @mock.patch('v1.util.migrations.json')
    def test_get_stream_data_revision(self, mock_json):
        """ Test that get_stream_data fetches the stream_data correctly
        from a revision object. """
        mock_revision = mock.Mock(spec=['content_json'])
        mock_json.loads.side_effect = [
            {'my_field': '[{"type": "test_field", "value": "testvalue"}]'},
            [{'type': 'test_field', 'value': 'testvalue'}],
        ]

        stream_data = get_stream_data(mock_revision, 'my_field')

        # There should be two calls to json.loads
        self.assertEqual(mock_json.loads.call_count, 2)
        self.assertEqual(stream_data[0]['type'], 'test_field')
        self.assertEqual(stream_data[0]['value'], 'testvalue')

    @mock.patch('wagtail.wagtailcore.blocks.stream_block.StreamBlock')
    @mock.patch('v1.util.migrations.StreamValue')
    @mock.patch('v1.util.migrations.setattr')
    def test_set_stream_data_page(self, mock_setattr, mock_StreamValue,
                                  mock_StreamBlock):
        """ Test that set_stream_data correctly sets stream data for a
        given page and saves the page. """
        mock_field = mock.Mock()
        mock_field.stream_block = mock_StreamBlock()

        mock_page = mock.Mock()
        mock_page.my_field = mock_field

        new_stream_data = [{'type': 'test_field', 'value': 'newtestvalue'}]
        set_stream_data(mock_page, 'my_field', new_stream_data)

        mock_StreamValue.assert_called_with(mock_field.stream_block,
                                            new_stream_data,
                                            is_lazy=True)
        mock_setattr.assert_called_with(mock_page, 'my_field',
                                        mock_StreamValue())
        mock_page.save.assert_called_once_with()

    @mock.patch('v1.util.migrations.json')
    def test_set_stream_data_revision(self, mock_json):
        """ Test that set_stream_data correctly sets stream data for a
        revision object and saves the revision. """
        mock_revision = mock.Mock(spec=['content_json', 'save'])
        mock_json.loads.return_value = \
            {'my_field': '[{"type": "test_field", "value": "testvalue"}]'}
        mock_json.dumps.side_effect = [
            '[{"type": "test_field", "value": "testvalue"}]',
            '{"my_field": "[{\\"type\\": \\"test_field\\", '
            '\\"value\\": \\"newtestvalue\\"}]"}',
        ]

        new_stream_data = [{'type': 'test_field', 'value': 'newtestvalue'}]
        set_stream_data(mock_revision, 'my_field', new_stream_data)

        # There should be 1 call to json.loads and 2 to json.dumps
        self.assertEqual(mock_json.loads.call_count, 1)
        self.assertEqual(mock_json.dumps.call_count, 2)
        self.assertEqual(mock_revision.content_json,
                         '{"my_field": "[{\\"type\\": \\"test_field\\", '
                         '\\"value\\": \\"newtestvalue\\"}]"}')
        mock_revision.save.assert_called_once_with()

    @mock.patch('v1.util.migrations.get_stream_data')
    @mock.patch('v1.util.migrations.set_stream_data')
    def test_migrate_stream_field(self,
                                  mock_set_stream_data,
                                  mock_get_stream_data):
        """ Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results. """
        mock_get_stream_data.return_value = \
            [{'type': 'my_type', 'value': {'afield': 'old data'}}]

        # Mock Wagtail page
        page = mock.Mock()

        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_stream_data.
        mapper = mock.Mock()
        mapper.return_value = {'afield': 'new data'}

        migrate_stream_field(page, 'my_field', 'my_type', mapper)

        # The mapper should be called with the page and "old" stream
        # field data
        mapper.assert_called_with(page, {'afield': 'old data'})

        # set_stream_data should be called with the "new" stream
        # field data
        mock_set_stream_data.assert_called_with(
            page, 'my_field',
            [{'type': 'my_type', 'value': {'afield': 'new data'}}])

    @mock.patch('v1.util.migrations.get_stream_data')
    @mock.patch('v1.util.migrations.set_stream_data')
    def test_migrate_stream_field_not_migrated(self,
                                               mock_set_stream_data,
                                               mock_get_stream_data):
        """ Test that the migrate_stream_field function correctly
        ignores a field that does not have the correct type and
        shouldn't be migrated. """
        mock_get_stream_data.return_value = \
            [{'type': 'my_type', 'value': {'afield': 'old data'}}]

        mapper = mock.Mock()

        migrate_stream_field(mock.Mock(), 'my_field', 'other_type', mapper)

        # The mapper should not be called
        mapper.assert_not_called()

        # set_stream_data should not be called
        mock_set_stream_data.assert_not_called()

    @mock.patch('django.apps.apps')
    @mock.patch('v1.util.migrations.migrate_stream_field')
    def test_migrate_page_types_and_fields(self,
                                           mock_migrate_stream_field,
                                           mock_apps):
        """ Test that the migrate_page_types_and_fields function
        correctly calls the migrate_stream_field function with
        the appropriate values from the list of page types and
        fields. """
        mapper = mock.Mock()

        # Set up a mock page model that return a single mock page
        mock_page = mock.Mock()
        mock_page_model = mock.Mock()
        mock_page_model.objects.all.return_value = [mock_page]

        # We also need a mock revision, and a mock of the filter query we
        # perform on the revision model's objects.
        mock_revision = mock.Mock()
        mock_revision_filter = mock.Mock()
        mock_revision_filter.order_by.return_value = [mock_revision]
        mock_revision_model = mock.Mock()
        mock_revision_model.objects.filter.return_value = mock_revision_filter

        mock_apps.get_model.side_effect = [mock_page_model,
                                           mock_revision_model]

        page_types_and_fields = [
            ('SomePage', 'my_field', 'my_type'),
        ]
        migrate_page_types_and_fields(mock_apps, page_types_and_fields, mapper)

        # Check that migrate_stream_field was correct called with the page
        mock_migrate_stream_field.assert_any_call(mock_page,
                                                  'my_field',
                                                  'my_type',
                                                  mapper)

        # Check that the revision lookup happened correctly and that the
        # revision stream field was correctly migrated.
        mock_revision_model.objects.filter.assert_called_with(page=mock_page)
        mock_migrate_stream_field.assert_any_call(mock_revision,
                                                  'my_field',
                                                  'my_type',
                                                  mapper)
