from unittest.mock import patch

from django.test import TestCase, override_settings

import boto3
import moto
from botocore.exceptions import ClientError

from agreements.metadata import Metadata


class MetadataTests(TestCase):
    @moto.mock_aws
    @override_settings(AWS_STORAGE_BUCKET_NAME="test.bucket")
    def test_metadata(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket("test.bucket")
        bucket.create()

        metadata = Metadata()

        self.assertEqual(metadata.prefix, "a/assets/bulk_agreements/")

        self.assertEqual(
            metadata.flexibilities,
            ["Q1-2020", "Q2-2020", "Q3-2020", "Q4-2020", "Q1-2021"],
        )

        self.assertEqual(
            metadata.notes,
            {
                "Q2-2019": "Agreements are incomplete due to"
                " technical submission issues at the Bureau"
            },
        )

        self.assertEqual(
            str(metadata.get_objects_by_prefix()),
            "s3.Bucket.objectsCollection(s3.Bucket(name='test.bucket')"
            ", s3.ObjectSummary)",
        )

    def fake(self):
        class Keyed:
            def __init__(self, k):
                self.key = k

        return [Keyed(1), Keyed(2), Keyed(3)]

    @moto.mock_aws
    @override_settings(AWS_STORAGE_BUCKET_NAME="test.bucket")
    @patch.object(Metadata, "get_objects_by_prefix", fake)
    def test_get_sorted(self):
        m = Metadata()
        self.assertEqual(m.get_sorted_agreements(), [3, 2, 1])

    def _raise(ex):
        raise ClientError({}, "test_error")

    @moto.mock_aws
    @patch.object(Metadata, "get_objects_by_prefix", _raise)
    def test_get_sorted_on_exception(self):
        m = Metadata()
        self.assertEqual(m.get_sorted_agreements(), [])
