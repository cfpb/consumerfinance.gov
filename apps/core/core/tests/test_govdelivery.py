from unittest import TestCase
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

import requests

from core.govdelivery import (
    ExceptionMockGovDelivery,
    LoggingMockGovDelivery,
    MockGovDelivery,
    ServerErrorMockGovDelivery,
    get_govdelivery_api,
)


class UnitTestGovDelivery(MockGovDelivery):
    pass


class GetGovDeliveryApiTests(SimpleTestCase):
    @override_settings(
        GOVDELIVERY_API="core.tests.test_govdelivery.UnitTestGovDelivery"
    )
    def test_uses_govdelivery_api_setting_for_class(self):
        self.assertIsInstance(get_govdelivery_api(), UnitTestGovDelivery)

    @override_settings(GOVDELIVERY_ACCOUNT_CODE="my-account-code")
    def test_uses_govdelivery_account_code_for_account_code(self):
        govdelivery = get_govdelivery_api()
        self.assertEqual(govdelivery.account_code, "my-account-code")


class MockGovDeliveryTests(TestCase):
    def test_new_object_has_no_calls(self):
        self.assertEqual(len(MockGovDelivery("code").calls), 0)

    def test_calls_get_recorded(self):
        govdelivery = MockGovDelivery("code")
        govdelivery.do_something(123, foo="bar")
        self.assertEqual(
            govdelivery.calls, [("do_something", (123,), {"foo": "bar"})]
        )

    def test_call_returns_valid_response(self):
        govdelivery = MockGovDelivery("code")
        response = govdelivery.do_something(123, foo="bar")
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200)


class ExceptionMockGovDeliveryTests(TestCase):
    def test_call_raises_valueerror(self):
        govdelivery = ExceptionMockGovDelivery("code")
        with self.assertRaises(RuntimeError):
            govdelivery.do_something(123, foo="bar")


class ServerErrorMockGovDeliveryTests(TestCase):
    def test_call_returns_invalid_response(self):
        govdelivery = ServerErrorMockGovDelivery("code")
        response = govdelivery.do_something(123, foo="bar")
        with self.assertRaises(requests.HTTPError):
            response.raise_for_status()


# Testing the logging of LoggingMockGovDelivery can be nicer upon adoption of
# Python 3.4+, using assertLogs:
#
# https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertLogs
class LoggingMockGovDeliveryTests(TestCase):
    def test_logging_happens(self):
        govdelivery = LoggingMockGovDelivery("code")
        with patch("core.govdelivery.logger") as logger:
            govdelivery.do_something(123, foo="bar")
            logger.info.assert_called_once_with(
                "GovDelivery(account_code=code).do_something(123, foo=bar)"
            )
