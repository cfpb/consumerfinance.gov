# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mock
from unittest import TestCase

from v1.util.migrations import (
    migrate_page_types_and_fields,
    migrate_stream_field,
)


class MigrationsUtilTestCase(TestCase):

    @mock.patch('v1.util.migrations.get_page_stream_data')
    @mock.patch('v1.util.migrations.set_page_stream_data')
    def test_migrate_stream_field(self,
                                  mock_set_page_stream_data,
                                  mock_get_page_stream_data):
        """ Test that the migrate_stream_field function correctly gets
        old data, calls the mapper function, and stores new data
        based on the mapper results. """
        mock_get_page_stream_data.return_value = \
            [{'type': 'my_type', 'value': {'afield': 'old data'}}]

        # Mock Wagtail page
        page = mock.Mock()

        # Mock the field mapper migration function. We'll inspect the
        # call to this and ensure the return value makes it to
        # set_page_stream_data.
        mapper = mock.Mock()
        mapper.return_value = {'afield': 'new data'}

        migrate_stream_field(page, 'my_field', 'my_type', mapper)

        # The mapper should be called with the page and "old" stream
        # field data
        mapper.assert_called_with(page, {'afield': 'old data'})

        # set_page_stream_data should be called with the "new" stream
        # field data
        mock_set_page_stream_data.assert_called_with(
            page, 'my_field',
            [{'type': 'my_type', 'value': {'afield': 'new data'}}])

    @mock.patch('v1.util.migrations.get_page_stream_data')
    @mock.patch('v1.util.migrations.set_page_stream_data')
    def test_migrate_stream_field_not_migrated(self,
                                               mock_set_page_stream_data,
                                               mock_get_page_stream_data):
        """ Test that the migrate_stream_field function correctly
        ignores a field that does not have the correct type and
        shouldn't be migrated. """
        mock_get_page_stream_data.return_value = \
            [{'type': 'my_type', 'value': {'afield': 'old data'}}]

        mapper = mock.Mock()

        migrate_stream_field(mock.Mock(), 'my_field', 'other_type', mapper)

        # The mapper should not be called
        mapper.assert_not_called()

        # set_page_stream_data should not be called
        mock_set_page_stream_data.assert_not_called()

    @mock.patch('v1.util.migrations.imported_apps.get_model')
    @mock.patch('v1.util.migrations.migrate_stream_field')
    def test_migrate_page_types_and_fields(self,
                                           mock_migrate_stream_field,
                                           mock_get_model):
        """ Test that the migrate_page_types_and_fields function
        correctly calls the migrate_stream_field function with
        the appropriate values from the list of page types and
        fields. """
        mapper = mock.Mock()

        # Set up a mock page model that return a single mock page
        mock_page = mock.Mock()
        mock_model = mock.Mock()
        mock_model.objects.all.return_value = [mock_page]
        mock_get_model.return_value = mock_model

        page_types_and_fields = [
            ('SomePage', 'my_field', 'my_type'),
        ]
        migrate_page_types_and_fields([], page_types_and_fields, mapper)

        mock_migrate_stream_field.assert_called_with(mock_page,
                                                     'my_field',
                                                     'my_type',
                                                     mapper)
