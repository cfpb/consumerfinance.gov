import os
from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from cfgov.util import admin_emails, environment_json


class AdminEmailsTestCase(SimpleTestCase):
    def test_empty(self):
        self.assertEqual(admin_emails(""), [])

    def test_with_emails(self):
        self.assertEqual(
            admin_emails("foo@cfpb.gov; bar@cfpb.gov"),
            [("foo", "foo@cfpb.gov"), (" bar", " bar@cfpb.gov")],
        )


class EnvironmentJsonTestCase(SimpleTestCase):
    @mock.patch.dict(os.environ, {})
    def test_with_variable_dne(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @mock.patch.dict(os.environ, {"TEST_VAR": ""})
    def test_with_empty(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @mock.patch.dict(os.environ, {"TEST_VAR": '["foo", "bar", ]'})
    def test_with_invalid_json(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @mock.patch.dict(os.environ, {})
    def test_with_default(self):
        self.assertEqual(environment_json("TEST_VAR", default="[]"), [])

    @mock.patch.dict(os.environ, {"TEST_VAR": '["foo", "bar"]'})
    def test_with_json_value(self):
        self.assertEqual(
            environment_json("TEST_VAR", default="Foo"),
            ["foo", "bar"],
        )
