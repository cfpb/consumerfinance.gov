import datetime
import time
import unittest
from unittest import mock

import requests

from alerts.newrelic_alerts import NewRelicAlertViolations


class TestNewRelicAlertViolations(unittest.TestCase):
    def setUp(self):
        # Set up patcher for all requests.get calls to New Relic
        patcher = mock.patch("requests.get")
        self.addCleanup(patcher.stop)
        self.mock_requests_get = patcher.start()
        self.newrelic_response = {
            "violations": [
                {
                    "condition_name": "cf.gov test opened now",
                    "entity": {
                        "name": "cf.gov synthetic entity",
                        "product": "Synthetic",
                        "type": "Monitor",
                    },
                    "id": 12345678,
                    "label": "This test opened just now",
                    "policy_name": "cf.gov unit tests",
                    "priority": "Critical",
                    "opened_at": time.time() * 1000.0,
                },
                {
                    "condition_name": "cf.gov test opened > 2 min ago",
                    "entity": {
                        "name": "cf.gov application entity",
                        "product": "Apm",
                        "type": "Application",
                    },
                    "id": 23456781,
                    "label": "This test opened 2 min ago",
                    "policy_name": "cf.gov unit tests",
                    "priority": "Critical",
                    "opened_at": time.time() * 1000.0,
                },
                {
                    "condition_name": "not cf.gov condition",
                    "entity": {
                        "name": "other application entity",
                        "product": "Apm",
                        "type": "Application",
                    },
                    "id": 34567812,
                    "label": "This is a different application",
                    "policy_name": "other unit tests",
                    "priority": "Critical",
                    "opened_at": time.time() * 1000.0,
                },
            ],
        }
        mock_response = mock.MagicMock(requests.Response)
        mock_response.json.return_value = self.newrelic_response
        self.mock_requests_get.return_value = mock_response

    def test_get_current_violations(self):
        nralert_violations = NewRelicAlertViolations(
            "token",
            "cf.gov",
            "123456",
        )
        violations = nralert_violations.get_current_violations()
        self.assertEqual(len(violations), 2)

    def test_get_new_violations(self):
        nralert_violations = NewRelicAlertViolations(
            "token",
            "cf.gov",
            "123456",
            known_violations=[23456781],
        )
        violations = nralert_violations.get_new_violations()
        self.assertEqual(len(violations), 1)

    def test_format_violation(self):
        nralert_violations = NewRelicAlertViolations(
            "token", "cf.gov", "123456"
        )
        formatted_violation = nralert_violations.format_violation(
            self.newrelic_response["violations"][0]
        )
        violation = self.newrelic_response["violations"][0]
        opened_timestamp = violation["opened_at"] / 1000.0
        opened = datetime.datetime.fromtimestamp(opened_timestamp)
        opened_str = opened.strftime("%a, %b %d %Y, at %I:%M %p %z")
        self.assertIn(
            "cf.gov test opened now, cf.gov synthetic entity "
            "- New Relic Synthetic, cf.gov synthetic entity, "
            "This test opened just now (Critical",
            formatted_violation,
        )
        self.assertIn(opened_str, formatted_violation)
