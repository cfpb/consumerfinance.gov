from importlib import import_module

from unittest import TestCase


class TestMigration0137(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMigration0137, cls).setUpClass()
        cls.migration = import_module(
            'v1.migrations.0137_migrate_imagetextgroups_to_infounitgroup'
        )

    def test_image_text_50_50_group_to_info_unit_group(self):
        data = {
            'heading': 'Image & Text 50/50 Group',
            'image_texts': [
                {
                    'heading': 'image_text 1',
                    'body': '<p>Body content</p>',
                    'image': {
                        'upload': 56
                    },
                    'links': [
                        {
                            'text': 'link 1',
                            'url': '#'
                        }
                    ],
                    'is_widescreen': True,
                    'is_button': False
                }
            ],
            'sharing': True,
            'link_image_and_heading': None
        }

        migrated = self.migration.image_text_group_to_info_unit_group(
            data,
            '50-50'
        )
        self.assertEqual(migrated, {
            'heading': {
                'text': 'Image & Text 50/50 Group',
                'level': 'h2'
            },
            'info_units': [
                {
                    'heading': {
                        'text': 'image_text 1',
                        'level': 'h3'
                    },
                    'body': '<p>Body content</p>',
                    'image': {
                        'upload': 56
                    },
                    'links': [
                        {
                            'text': 'link 1',
                            'url': '#'
                        }
                    ]
                }
            ],
            'sharing': True,
            'link_image_and_heading': False,
            'format': '50-50'
        })

    def test_image_text_25_75_group_to_info_unit_group(self):
        data = {
            'heading': 'Image & Text 25/75 Group',
            'image_texts': [
                {
                    'heading': 'image_text 1',
                    'has_rule': True,
                    'body': '<p>Body content</p>',
                    'image': {
                        'upload': 58
                    },
                    'is_widescreen': True,
                    'is_button': False
                }
            ],
            'sharing': True,
            'link_image_and_heading': True
        }

        migrated = self.migration.image_text_group_to_info_unit_group(
            data,
            '25-75'
        )
        self.assertEqual(migrated, {
            'heading': {
                'text': 'Image & Text 25/75 Group',
                'level': 'h2'
            },
            'info_units': [
                {
                    'heading': {
                        'text': 'image_text 1',
                        'level': 'h3'
                    },
                    'body': '<p>Body content</p>',
                    'image': {
                        'upload': 58
                    },
                    'links': [],
                }
            ],
            'lines_between_items': True,
            'sharing': True,
            'link_image_and_heading': True,
            'format': '25-75'
        })
