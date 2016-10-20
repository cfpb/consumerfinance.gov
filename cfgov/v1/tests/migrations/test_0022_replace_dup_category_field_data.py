# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib

import mock
from unittest import TestCase

from wagtail.wagtailcore.models import Page, PageRevision


class RemoveDupCategoryFieldMigrationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RemoveDupCategoryFieldMigrationTestCase, cls).setUpClass()
        cls.migration = importlib.import_module(
            'v1.migrations.0022_replace_dup_category_field_data'
        )

    def test_forwards_with_category(self):
        """ Forward migration with a category """
        data = {
            'category': 'test-category',
        }
        migrated = self.migration.migrate_category_field_forwards(None, data)
        self.assertEqual(migrated, {'show_category': True})

    def test_forwards_without_category(self):
        """ Forward migration without a category """
        data = {
            'category': '',
        }
        migrated = self.migration.migrate_category_field_forwards(None, data)
        self.assertEqual(migrated, {'show_category': False})

    def test_backwards_with_show_category_page(self):
        """ Backward migration with show_category=True for a page """
        mock_page = mock.Mock(spec=Page)
        mock_page.categories = [{'name': 'test-category'}]
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(
            mock_page, data)
        self.assertEqual(migrated, {'category': 'test-category'})

    @mock.patch('v1.migrations.0022_replace_dup_category_field_data.json')
    def test_backwards_with_show_category_revision(self, mock_json):
        """ Backward migration show_category=True for a revision """
        mock_revision = mock.Mock(spec=PageRevision)
        mock_revision.content_json = ""
        mock_json.loads.return_value = {
            'categories': [{'name': 'test-category'}]}
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(mock_revision, data)
        self.assertEqual(migrated, {'category': 'test-category'})

    @mock.patch('v1.migrations.0022_replace_dup_category_field_data.json')
    def test_backwards_with_show_category_revision_without_category(
            self, mock_json):
        """ Backward migration show_category=True for a revision """
        mock_revision = mock.Mock(spec=PageRevision)
        mock_revision.content_json = ""
        mock_json.loads.return_value = {'categories': []}
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(mock_revision, data)
        self.assertEqual(migrated, {'category': ''})

    def test_backwards_without_show_category(self):
        """ Backward migration with show_category=False and an empty category
        string. """
        mock_page = mock.Mock(spec=Page)
        mock_page.categories = [{'name': 'test-category'}]
        data = {
            'show_category': False,
        }
        migrated = self.migration.migrate_category_field_backwards(
            mock_page, data)
        self.assertEqual(migrated, {'category': ''})

    def test_backwards_without_category(self):
        """ Backward migration with show_category=True and categories """
        mock_page = mock.Mock(spec=Page)
        mock_page.categories = []
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(
            mock_page, data)
        self.assertEqual(migrated, {'category': ''})
