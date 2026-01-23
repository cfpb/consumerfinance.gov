import csv
import datetime
import os
from io import StringIO

import boto3
import requests


# We want the process to be able to succeed in stgpub but default to prodpub
ALTO_ENV = os.getenv("ALTO_ENV", "prodpub")
ALTO_DOWNLOAD_BUCKET = f"cfpb-{ALTO_ENV}-cfgov-files-main"
DOWNLOAD_KEY = "data/mortgage-performance/downloads"


def read_in_s3_csv(url):
    response = requests.get(url)
    f = StringIO(response.content.decode("utf-8"))
    reader = csv.DictReader(f)
    return reader


def bake_csv_to_s3(slug, csv_file_obj, bucket=None, key=None):
    """Posts CSV files to an Alto s3 cfgov-files-main sub_bucket."""
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    expire_date = utc_now + datetime.timedelta(days=365)
    expires = expire_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    if bucket is None:
        bucket = ALTO_DOWNLOAD_BUCKET
    if key is None:
        key = DOWNLOAD_KEY
    # Rewind the file to its beginning.
    csv_file_obj.seek(0)
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=f"{key}/{slug}.csv",
        ContentType="text/csv",
        Body=csv_file_obj.getvalue(),
        CacheControl="max-age=2592000,public",
        Expires=expires,
    )
