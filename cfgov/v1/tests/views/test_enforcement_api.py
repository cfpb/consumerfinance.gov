import json
from datetime import date

from django.test import TestCase

from wagtail.core.models import Site

from model_bakery import baker

from v1.models.enforcement_action_page import (
    EnforcementActionAtRisk, EnforcementActionDefendantType,
    EnforcementActionDisposition, EnforcementActionDocket,
    EnforcementActionPage, EnforcementActionProduct, EnforcementActionStatus,
    EnforcementActionStatute
)
from v1.views.enforcement_api import EnforcementActionSerializer


class EnforcementAPITestCase(TestCase):
    # Things to note in the expected JSON output:
    # Lists of products, statuses, etc. are flattened to lists of strings, not
    # JSON objects. ChoiceFields like statuses, statutes, etc. use their
    # display values.
    expected_json = json.loads('''
    {
        "public_enforcement_action": "Sample Enforcement Action",
        "initial_filing_date": "2021-01-01",
        "defendant_types": ["Bank", "Nonbank"],
        "court": "CFPB Office of Administrative Adjudication",
        "docket_numbers": ["2021-CFPB-0001"],
        "settled_or_contested_at_filing": "Settled",
        "products": ["Other Consumer Product (not lending)"],
        "at_risk_groups": ["Students"],
        "enforcement_dispositions": [
            {
                "final_disposition": "Sample Sample Action",
                "final_disposition_type": "Final Order",
                "final_order_date": "2021-02-02",
                "dismissal_date": null,
                "final_order_consumer_redress": 333.0,
                "final_order_consumer_redress_suspended": 444.0,
                "final_order_other_consumer_relief": 555.0,
                "final_order_other_consumer_relief_suspended": 666.0,
                "final_order_disgorgement": 777.0,
                "final_order_disgorgement_suspended": 888.0,
                "final_order_civil_money_penalty": 999.0,
                "final_order_civil_money_penalty_suspended": 111.0,
                "estimated_consumers_entitled_to_relief": "Zero"
            }
        ],
        "statuses": ["Expired/Terminated/Dismissed"],
        "statutes": ["Consumer Leasing Act/Regulation M"],
        "url": "/enforcement/actions/sample-action/"
    }
    ''')

    def setUp(self):
        self.enforcement_page = baker.prepare(EnforcementActionPage)

        self.enforcement_page.public_enforcement_action = 'Sample Enforcement Action'
        self.enforcement_page.initial_filing_date = date(2021, 1, 1)
        self.enforcement_page.defendant_types = [
            EnforcementActionDefendantType(defendant_type='Bank'),
            EnforcementActionDefendantType(defendant_type='Non-Bank'),
        ]
        self.enforcement_page.court = "CFPB Office of Administrative Adjudication"
        self.enforcement_page.docket_numbers.add(
            EnforcementActionDocket(docket_number='2021-CFPB-0001'))
        self.enforcement_page.settled_or_contested_at_filing = 'Settled'
        self.enforcement_page.products.add(
            EnforcementActionProduct(product='Other Consumer Products (Not Lending)'))
        self.enforcement_page.at_risk_groups.add(
            EnforcementActionAtRisk(at_risk_group='Students'))
        self.enforcement_page.enforcement_dispositions.add(
            EnforcementActionDisposition(
                final_disposition = "Sample Sample Action",
                final_disposition_type = "Final Order",
                final_order_date = "2021-02-02",
                final_order_consumer_redress = "333.00",
                final_order_consumer_redress_suspended = "444.00",
                final_order_other_consumer_relief = "555.00",
                final_order_other_consumer_relief_suspended = "666.00",
                final_order_disgorgement = "777.00",
                final_order_disgorgement_suspended = "888.00",
                final_order_civil_money_penalty = "999.00",
                final_order_civil_money_penalty_suspended = "111.00",
                estimated_consumers_entitled_to_relief = "Zero"
            ))
        self.enforcement_page.statuses.add(
            EnforcementActionStatus(status='expired-terminated-dismissed'))
        self.enforcement_page.statutes.add(
            EnforcementActionStatute(statute='CLA'))


    def test_serializes_correct_keys(self):
        serializer = EnforcementActionSerializer(self.enforcement_page)
        output_keys = serializer.data.keys()
        expected_keys = self.expected_json.keys()
        self.assertEqual(output_keys, expected_keys)

    def test_uses_display_names(self):
        serializer = EnforcementActionSerializer(self.enforcement_page)
        self.assertEqual(
                serializer.data['statuses'],
                self.expected_json['statuses']
        )
        self.assertEqual(
                serializer.data['products'],
                self.expected_json['products']
        )

    def test_flattens_lists(self):
        serializer = EnforcementActionSerializer(self.enforcement_page)
        self.assertEqual(
                serializer.data['defendant_types'],
                self.expected_json['defendant_types']
        )

    def test_serializes_disposition(self):
        serializer = EnforcementActionSerializer(self.enforcement_page)
        output_keys = serializer.data['enforcement_dispositions'][0].keys()
        expected_keys = self.expected_json['enforcement_dispositions'][0].keys()  # noqa E501
        self.assertEqual(output_keys, expected_keys)

    def test_serializes_decimals_as_numbers(self):
        serializer = EnforcementActionSerializer(self.enforcement_page)
        output = serializer.data['enforcement_dispositions'][0]['final_order_disgorgement']  # noqa E501
        expected = self.expected_json['enforcement_dispositions'][0]['final_order_disgorgement']   # noqa E501
        self.assertEqual(output, expected)

    def test_can_serialize_empty_metadata(self):
        empty_page = baker.prepare(EnforcementActionPage)
        serializer = EnforcementActionSerializer(empty_page)
        output_keys = serializer.data.keys()
        expected_keys = self.expected_json.keys()
        self.assertEqual(output_keys, expected_keys)

