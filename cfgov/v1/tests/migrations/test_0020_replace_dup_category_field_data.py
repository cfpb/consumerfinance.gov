# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib

from mock import Mock
from unittest import TestCase


class RemoveDupCategoryFieldMigrationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RemoveDupCategoryFieldMigrationTestCase, cls).setUpClass()
        cls.migration = importlib.import_module(
            'v1.migrations.0020_replace_dup_category_field_data'
        )

    def test_forwards_with_category(self):
        data = {
            'category': 'test-category',
        }
        migrated = self.migration.migrate_category_field_forwards(None, data)
        self.assertEqual(migrated, {'show_category': True})

    def test_forwards_without_category(self):
        data = {
            'category': '',
        }
        migrated = self.migration.migrate_category_field_forwards(None, data)
        self.assertEqual(migrated, {'show_category': False})

    def test_backwards_with_show_category(self):
        page = Mock(categories=Mock(values=[{'name': 'test-category'}]))
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(page, data)
        self.assertEqual(migrated, {'category': 'test-category'})

    def test_backwards_without_show_category(self):
        page = Mock(categories=Mock(values=[{'name': 'test-category'}]))
        data = {
            'show_category': False,
        }
        migrated = self.migration.migrate_category_field_backwards(page, data)
        self.assertEqual(migrated, {'category': ''})

    def test_backwards_without_category(self):
        page = Mock(categories=Mock(values=[]))
        data = {
            'show_category': True,
        }
        migrated = self.migration.migrate_category_field_backwards(page, data)
        self.assertEqual(migrated, {'category': ''})
