from importlib import import_module

from unittest import TestCase


class TestMigration0117(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMigration0117, cls).setUpClass()
        cls.migration = import_module('v1.migrations.0117_contentimage_data')

    def test_forward_mapper(self):
        data = [
            {
                'type': 'media',
                'value': 56
            },
            {
                'type': 'content',
                'value': '<p>Text content</p>'
            },
            {
                'type': 'media',
                'value': 58
            },
        ]

        migrated = self.migration.forward_mapper(None, data)
        self.assertEqual(migrated, [
            {
                'type': 'image_inset',
                'value': {
                    'image': {
                        'upload': 56
                    },
                    'image_width': 'full',
                    'is_bottom_rule': False
                }
            },
            {
                'type': 'content',
                'value': '<p>Text content</p>'
            },
            {
                'type': 'image_inset',
                'value': {
                    'image': {
                        'upload': 58
                    },
                    'image_width': 'full',
                    'is_bottom_rule': False
                }
            },
        ])
