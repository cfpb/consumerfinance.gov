import importlib

from unittest import TestCase


class HeroRefactorMigrationTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HeroRefactorMigrationTestCase, cls).setUpClass()
        cls.migration = importlib.import_module(
            'v1.migrations.0011_hero_refactor_data'
        )

    def test_only_image_forwards(self):
        data = {
            'image': {'upload': 123, 'alt': 'foo'},
            'background_image': None,
        }

        migrated = self.migration.migrate_hero_forwards(data)
        self.assertEqual(migrated, {'image': 123, 'small_image': None})

    def test_image_and_background_image_forwards(self):
        data = {
            'image': {'upload': 123, 'alt': 'foo'},
            'background_image': 456,
        }

        migrated = self.migration.migrate_hero_forwards(data)
        self.assertEqual(migrated, {'image': 456, 'small_image': 123})

    def test_only_background_image_forwards(self):
        data = {
            'image': None,
            'background_image': 456,
        }

        migrated = self.migration.migrate_hero_forwards(data)
        self.assertEqual(migrated, {'image': 456, 'small_image': None})

    def test_no_images_forwards(self):
        data = {
            'image': None,
            'background_image': None,
        }

        migrated = self.migration.migrate_hero_forwards(data)
        self.assertEqual(migrated, {'image': None, 'small_image': None})

    def test_image_and_small_image_backwards(self):
        data = {
            'image': 123,
            'small_image': 456
        }

        migrated = self.migration.migrate_hero_backwards(data)
        self.assertEqual(migrated, {
            'image': {'upload': 456, 'alt': ''},
            'background_image': 123,
        })

    def test_only_image_backwards(self):
        data = {
            'image': 123,
            'small_image': None,
        }

        migrated = self.migration.migrate_hero_backwards(data)
        self.assertEqual(migrated, {
            'image': {'upload': 123, 'alt': ''},
            'background_image': None,
        })

    def test_only_small_image_backwards(self):
        data = {
            'image': None,
            'small_image': 456,
        }

        migrated = self.migration.migrate_hero_backwards(data)
        self.assertEqual(migrated, {
            'image': {'upload': 456, 'alt': ''},
            'background_image': None,
        })

    def test_no_images_backwards(self):
        data = {
            'image': None,
            'small_image': None,
        }

        migrated = self.migration.migrate_hero_backwards(data)
        self.assertEqual(migrated, {
            'image': None,
            'background_image': None,
        })
