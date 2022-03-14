import datetime

from django.test import TestCase

from wagtail.core.models import Page, Site

from scripts.export_enforcement_actions import assemble_output
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.tests.wagtail_pages.helpers import save_new_page


class TestExportEnforcementActions(TestCase):
    def setUp(self):
        self.site_root = Site.objects.get(is_default_site=True).root_page

        self.policy_compliance_page = Page(
            title="Policy & Compliance", slug="policy-compliance"
        )
        save_new_page(self.policy_compliance_page, root=self.site_root)

        self.enforcement_page = Page(title="Enforcement", slug="enforcement")
        save_new_page(self.enforcement_page, root=self.policy_compliance_page)

        self.actions_page = Page(title="Actions", slug="actions")
        save_new_page(self.actions_page, root=self.enforcement_page)

        self.test_all_data_page = EnforcementActionPage(
            title="Great Test Page",
            initial_filing_date="2012-07-18",
            live=True,
        )
        save_new_page(self.test_all_data_page, root=self.actions_page)

        self.test_no_data_page = EnforcementActionPage(
            title="Terrible Test Page", live=False
        )
        save_new_page(self.test_no_data_page, root=self.actions_page)

        self.test_wrong_page = EnforcementActionPage(
            title="Wrong Test Page", live=True
        )
        save_new_page(self.test_wrong_page, root=self.enforcement_page)

    def test_assemble_output(self):
        output = assemble_output()
        self.assertEqual(
            [
                {
                    "Forum": "",
                    "Title": "Great Test Page",
                    "Court": "",
                    "Docket Numbers": "",
                    "Statuses": "",
                    "Products": "",
                    "Content": "",
                    "URL": (
                        "https://consumerfinance.gov/policy-compliance/"
                        "enforcement/actions/great-test-page/"
                    ),
                    "Initial Filing Date": datetime.date(2012, 7, 18),
                }
            ],
            output,
        )
