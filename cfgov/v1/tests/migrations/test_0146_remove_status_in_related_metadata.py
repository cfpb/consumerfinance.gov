from importlib import import_module

from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock



class TestMigrationXXXX(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMigrationXXXX, cls).setUpClass()
        cls.migration = import_module('v1.migrations.0146_remove_status_in_related_metadata')

    def test_remove_status_in_related_metadata(self):
        mock_page_or_revision = mock.MagicMock(
            url_path='/cfgov/policy-compliance/enforcement/actions/my_action'
        )
        data = {
            'content': [
                {
                    'type': 'text',
                    'value': {
                        'heading': 'Category',
                        'blob': 'Some Categorization'
                    }
                },
                {
                    'type': 'text',
                    'value': {
                        'heading': 'Status',
                        'blob': 'Inactive or resolved'
                    }
                },
                {
                    'type': 'nottext',
                    'value': {},
                }
            ]
        }

        migrated = self.migration.remove_status_in_related_metadata(
            mock_page_or_revision, data
        )
        self.assertEqual(
            migrated,
            {
                'content': [
                    {
                        'type': 'text',
                        'value': {
                            'heading': 'Category',
                            'blob': 'Some Categorization'
                        }
                    },
                    {
                        'type': 'nottext',
                        'value': {},
                    }
                ]
            }
        )
