from importlib import import_module

from unittest import TestCase


class TestMigration0137(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMigration0137, cls).setUpClass()
        cls.migration = import_module(
            'v1.migrations.0137_migrate_linkblobgroups_to_infounitgroup'
        )

    def test_half_width_link_blob_group_to_info_unit_group(self):
        data = {
            'heading': 'Half-width Link Blob Group',
            'link_blobs': [
                {
                    'heading': 'link_blob 1',
                    'body': '<p>Body content</p>',
                    'links': [
                        {
                            'text': 'link 1',
                            'url': '#'
                        }
                    ],
                }
            ],
            'has_top_border': True,
            'has_bottom_border': True
        }

        migrated = self.migration.link_blob_group_to_info_unit_group(
            data,
            '50-50'
        )
        self.assertEqual(migrated, {
            'heading': {
                'text': 'Half-width Link Blob Group',
                'level': 'h2'
            },
            'info_units': [
                {
                    'heading': {
                        'text': 'link_blob 1',
                        'level': 'h3'
                    },
                    'body': '<p>Body content</p>',
                    'links': [
                        {
                            'text': 'link 1',
                            'url': '#'
                        }
                    ]
                }
            ],
            'has_top_rule_line': True,
            'link_image_and_heading': False,
            'format': '50-50'
        })

    def test_third_width_link_blob_group_to_info_unit_group(self):
        data = {
            'heading': 'Third-width Link Blob Group',
            'link_blobs': [
                {
                    'sub_heading': 'link_blob 1',
                    'sub_heading_icon': 'help-round',
                    'body': '<p>Body content</p>',
                }
            ],
            'has_top_border': False,
            'has_bottom_border': None
        }

        migrated = self.migration.link_blob_group_to_info_unit_group(
            data,
            '33-33-33'
        )
        self.assertEqual(migrated, {
            'heading': {
                'text': 'Third-width Link Blob Group',
                'level': 'h2'
            },
            'info_units': [
                {
                    'heading': {
                        'text': 'link_blob 1',
                        'level': 'h4',
                        'icon': 'help-round'
                    },
                    'body': '<p>Body content</p>',
                    'links': [],
                }
            ],
            'link_image_and_heading': False,
            'format': '33-33-33'
        })
