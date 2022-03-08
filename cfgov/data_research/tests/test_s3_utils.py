import csv
from io import BytesIO, StringIO

from django.test import TestCase, override_settings

import boto3
import moto
import responses

from data_research.mortgage_utilities.s3_utils import (
    bake_csv_to_s3,
    read_in_s3_csv,
)


class S3UtilsTests(TestCase):
    @responses.activate
    def test_read_in_s3_csv(self):
        url = "https://test.url/foo.csv"
        responses.add(responses.GET, url, body="a,b,c\nd,e,f")
        reader = read_in_s3_csv(url)
        self.assertEqual(reader.fieldnames, ["a", "b", "c"])
        self.assertEqual(sorted(next(reader).values()), ["d", "e", "f"])

    @moto.mock_s3
    @override_settings(AWS_STORAGE_BUCKET_NAME="test.bucket")
    def test_bake_csv_to_s3(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket("test.bucket")
        bucket.create(ACL="private")

        # In Python 3, csv.writer expects a file opened in text mode, which is
        # a StringIO.
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(["a", "b", "c"])
        writer.writerow(["1", "2", "3"])

        # But boto3 expects a regular file object, so we need to convert to
        # BytesIO.
        bake_csv_to_s3("foo", BytesIO(csvfile.getvalue().encode("utf-8")))

        key = bucket.Object("data/foo.csv")
        response = key.get()
        self.assertEqual(response["Body"].read(), b"a,b,c\r\n1,2,3\r\n")

        # bake_csv_to_s3 sets 'public-read' on the item.
        acl = key.Acl()
        self.assertIn(
            {
                "Permission": "READ",
                "Grantee": {
                    "Type": "Group",
                    "URI": "http://acs.amazonaws.com/groups/global/AllUsers",
                },
            },
            acl.grants,
        )
