import datetime

from django.test import TestCase

from wagtail.core.models import Page, Site

from scripts.export_enforcement_actions import assemble_output
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


class TestExportEnforcementActions(TestCase):

    def setUp(self):
        self.site_root = Site.objects.get(is_default_site=True).root_page

        self.policy_compliance_page = Page(
            title='Policy & Compliance',
            slug='policy-compliance'
        )
        save_new_page(self.policy_compliance_page, root=self.site_root)

        self.enforcement_page = Page(title='Enforcement', slug='enforcement')
        save_new_page(self.enforcement_page, root=self.policy_compliance_page)

        self.actions_page = Page(title='Actions', slug='actions')
        save_new_page(self.actions_page, root=self.enforcement_page)

        self.test_all_data_page = EnforcementActionPage(
            title="Great Test Page",
            live=True,
            preview_description='This is a great test page.'
        )
        save_new_page(self.test_all_data_page, root=self.actions_page)
        set_stream_data(
            self.test_all_data_page,
            'sidefoot',
            [
                {
                    'type': 'related_metadata',
                    'value': {
                        'content': [
                            {
                                'type': 'text',
                                'value': {
                                    'heading': 'Status',
                                    'blob': '<p>Inactive or resolved</p>'
                                },
                            },
                            {
                                'type': 'text',
                                'value': {
                                    'heading': 'File number',
                                    'blob': '<p>2012-CFPB-0001</p>'
                                },
                            },
                            {
                                'type': 'date',
                                'value': {
                                    'heading': 'Date filed',
                                    'date': datetime.date(2012, 7, 18)
                                },
                            }
                        ],
                    },
                },
            ]
        )
        set_stream_data(
            self.test_all_data_page,
            'content',
            [
                {
                    'type': 'full_width_text',
                    'value': [
                        {
                            'type': 'content',
                            'value': 'CONTENT'
                        }
                    ]
                },
            ]
        )

        self.test_no_data_page = EnforcementActionPage(
            title="Terrible Test Page",
            live=False,
            preview_description='This is a terrible test page.'
        )
        save_new_page(self.test_no_data_page, root=self.actions_page)

        self.test_wrong_page = EnforcementActionPage(
            title="Wrong Test Page",
            live=True,
            preview_description='This is the wrong test page.'
        )
        save_new_page(self.test_wrong_page, root=self.enforcement_page)

    def test_assemble_output(self):
        output = assemble_output()
        self.assertEqual(
            [{
                'Category': '',
                'Matter name': 'Great Test Page',
                'Preview text': 'This is a great test page.',
                'URL': ('https://consumerfinance.gov/policy-compliance/'
                        'enforcement/actions/great-test-page/'),
                'Date filed': '2012-07-18',
                'Status': 'Inactive or resolved',
                'File number': '2012-CFPB-0001',
                'Content': 'CONTENT',
            }],
            output
        )
