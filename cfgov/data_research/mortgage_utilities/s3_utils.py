from __future__ import unicode_literals
import datetime
import os
import StringIO

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.key import Key
import requests
import unicodecsv

# bake_to_s3 functions require S3 secrets to be stored in the env
S3_KEY = os.getenv('AWS_S3_ACCESS_KEY_ID')
S3_SECRET = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
BASE_BUCKET = 'files.consumerfinance.gov'
MORTGAGE_SUB_BUCKET = "data/mortgage-performance"
# s3_base is "http://files.consumerfinance.gov"
# files live at
# http://s3.amazonaws.com/files.consumerfinance.gov/data/mortgage-performance/


def read_in_s3_csv(url):
    response = requests.get(url)
    f = StringIO.StringIO(response.content)
    reader = unicodecsv.DictReader(f)
    return reader


def read_in_s3_json(url):
    """Reads in a json file from S3 and returns a Python object"""
    response = requests.get(url)
    return response.json()


def bake_json_to_s3(slug, json_string, sub_bucket=None):
    """A utility for posting json files to a cfgov.files sub_bucket."""
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=365)
    expires = expire_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {'Cache-Control': 'max-age=2592000,public',
               'Expires': expires,
               'Access-Control-Allow-Origin': '*'}
    if sub_bucket is None:
        sub_bucket = 'data'
    s3 = boto.connect_s3(
        S3_KEY, S3_SECRET, calling_format=OrdinaryCallingFormat())
    bucket = s3.get_bucket(BASE_BUCKET)
    key = Key(
        bucket=bucket,
        name='{}/{}.json'.format(sub_bucket, slug))
    key.content_type = 'application/json'
    key.set_contents_from_string(json_string, headers=headers)
    key.set_acl('public-read')


def bake_csv_to_s3(slug, csv_file_obj, sub_bucket=None):
    """A utility for posting csv files to a cfgov.files sub_bucket."""
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=365)
    expires = expire_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {'Cache-Control': 'max-age=2592000,public',
               'Expires': expires}
    if sub_bucket is None:
        sub_bucket = 'data'
    s3 = boto.connect_s3(
        S3_KEY, S3_SECRET, calling_format=OrdinaryCallingFormat())
    bucket = s3.get_bucket(BASE_BUCKET)
    key = Key(
        bucket=bucket,
        name='{}/{}.csv'.format(sub_bucket, slug))
    key.content_type = 'text/csv'
    key.set_contents_from_file(csv_file_obj, headers=headers, rewind=True)
    key.set_acl('public-read')
