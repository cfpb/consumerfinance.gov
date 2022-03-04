import csv
import datetime
from io import StringIO

from django.conf import settings

import boto3
import requests


# bake_to_s3 functions require S3 secrets to be stored in the env
BASE_BUCKET = settings.AWS_STORAGE_BUCKET_NAME
MORTGAGE_SUB_BUCKET = "data/mortgage-performance"
PUBLIC_ACCESS_BASE = "https://s3.amazonaws.com/{}/{}".format(
    BASE_BUCKET, MORTGAGE_SUB_BUCKET
)
S3_MORTGAGE_DOWNLOADS_BASE = "{}/downloads".format(PUBLIC_ACCESS_BASE)
S3_SOURCE_BUCKET = "{}/source".format(PUBLIC_ACCESS_BASE)
S3_SOURCE_FILE = "latest_county_delinquency.csv"


def read_in_s3_csv(url):
    response = requests.get(url)
    f = StringIO(response.content.decode("utf-8"))
    reader = csv.DictReader(f)
    return reader


def bake_csv_to_s3(slug, csv_file_obj, sub_bucket=None):
    """A utility for posting CSV files to a cfgov.files sub_bucket.

    Uses the value of settings.AWS_STORAGE_BUCKET_NAME as the destination S3
    bucket. If sub_bucket is not provided, defaults to 'data'.
    """
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=365)
    expires = expire_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if sub_bucket is None:
        sub_bucket = "data"

    # Rewind the file to its beginning.
    csv_file_obj.seek(0)

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key="{}/{}.csv".format(sub_bucket, slug),
        ACL="public-read",
        ContentType="text/csv",
        Body=csv_file_obj.getvalue(),
        CacheControl="max-age=2592000,public",
        Expires=expires,
    )
