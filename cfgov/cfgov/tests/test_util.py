import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from storages.backends.s3 import S3Storage

from cfgov.util import admin_emails, environment_json, get_s3_media_config


class AdminEmailsTestCase(SimpleTestCase):
    def test_empty(self):
        self.assertEqual(admin_emails(""), [])

    def test_with_emails(self):
        self.assertEqual(
            admin_emails("foo@cfpb.gov; bar@cfpb.gov"),
            [("foo", "foo@cfpb.gov"), (" bar", " bar@cfpb.gov")],
        )


class EnvironmentJsonTestCase(SimpleTestCase):
    @patch.dict(os.environ, {})
    def test_with_variable_dne(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @patch.dict(os.environ, {"TEST_VAR": ""})
    def test_with_empty(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @patch.dict(os.environ, {"TEST_VAR": '["foo", "bar", ]'})
    def test_with_invalid_json(self):
        with self.assertRaises(ImproperlyConfigured):
            environment_json("TEST_VAR")

    @patch.dict(os.environ, {})
    def test_with_default(self):
        self.assertEqual(environment_json("TEST_VAR", default="[]"), [])

    @patch.dict(os.environ, {"TEST_VAR": '["foo", "bar"]'})
    def test_with_json_value(self):
        self.assertEqual(
            environment_json("TEST_VAR", default="Foo"),
            ["foo", "bar"],
        )


class S3MediaConfigTests(SimpleTestCase):
    def assertS3Config(self, env, expected_media_url, file_path, expected_url):
        with patch.dict("os.environ", env, clear=True):
            media_url, storage_options = get_s3_media_config()
            storage = S3Storage(**storage_options)

            self.assertEqual(storage.url(file_path), expected_url)
            self.assertEqual(media_url, expected_media_url)

    def test_requires_bucket_name(self):
        with self.assertRaises(KeyError) as e:
            self.assertS3Config({}, "ignore", "ignore", "ignore")
        self.assertEqual(e.exception.args, ("AWS_STORAGE_BUCKET_NAME",))

    def test_no_custom_domain(self):
        self.assertS3Config(
            {
                "AWS_STORAGE_BUCKET_NAME": "my-bucket",
            },
            "https://my-bucket.s3.amazonaws.com/f/",
            "documents/test.pdf",
            "https://my-bucket.s3.amazonaws.com/f/documents/test.pdf",
        )

    def test_custom_location(self):
        self.assertS3Config(
            {
                "AWS_STORAGE_BUCKET_NAME": "my-bucket",
                "AWS_S3_STORAGE_LOCATION": "my-files",
            },
            "https://my-bucket.s3.amazonaws.com/my-files/",
            "documents/test.pdf",
            "https://my-bucket.s3.amazonaws.com/my-files/documents/test.pdf",
        )

    def test_custom_domain(self):
        self.assertS3Config(
            {
                "AWS_STORAGE_BUCKET_NAME": "my-bucket",
                "AWS_S3_CUSTOM_DOMAIN": "my-bucket.com",
            },
            "https://my-bucket.com/f/",
            "documents/test.pdf",
            "https://my-bucket.com/f/documents/test.pdf",
        )
