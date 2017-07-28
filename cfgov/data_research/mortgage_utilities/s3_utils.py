from __future__ import unicode_literals
import os
import StringIO

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.key import Key
import requests
import unicodecsv

# bake_to_s3 functions require S3 secrets to be stored in the env
S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET')
BASE_BUCKET = 'files.consumerfinance.gov'
MORTGAGE_SUB_BUCKET = "data/mortgage-performance"
# s3_base is "http://files.consumerfinance.gov" -- not using https yet
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


def prep_key(key, content):
    """Prep content for an s3 endpoint 'key'."""
    key.set_contents_from_string(content)
    key.set_acl('public-read')
    key.content_type = 'application/json'
    return key


def bake_json_to_s3(slug, json_string, sub_bucket=None):
    """A utility for posting json files to the mortgage-performance bucket."""
    if sub_bucket is None:
        sub_bucket = MORTGAGE_SUB_BUCKET
    s3 = boto.connect_s3(
        S3_KEY, S3_SECRET, calling_format=OrdinaryCallingFormat())
    bucket = s3.get_bucket(BASE_BUCKET)
    json_prep = Key(
        bucket=bucket, name='{}/{}.json'.format(
            sub_bucket, slug))
    json_prep = prep_key(json_prep, json_string)


# One-off routine to post demo MSA files to s3

# KEYNAME = "data/mortgage-performance/metro"


# def bake_msa_to_s3(fips, day_range, json_string):
#     from boto.s3.key import Key
#     s3 = boto.connect_s3(
#         S3_KEY, S3_SECRET, calling_format=OrdinaryCallingFormat())
#     bucket = s3.get_bucket(BASE_BUCKET)
#     json_prep = Key(
#         bucket=bucket, name='{}/{}_{}_day_delinq_percent.json'.format(
#             KEYNAME, fips, day_range))
#     json_prep = prep_key(json_prep, json_string)


# def post_msa_timeseries(fips):
#     import json
#     from data_research.models import MSAMortgageData
#     records = MSAMortgageData.objects.filter(fips=fips)
#     name = FIPS.msa_fips[fips]['msa']
#     data = {'label': name,
#             'data': [record.time_series for record in records]}
#     json_string = json.dumps(data)
#     day_range = '30'
#     bake_msa_to_s3(fips, day_range, json_string)


# def load_msa_timeseries_files():
#     from data_research.mortgage_utilities.fips_meta import (
#         FIPS, load_fips_meta)
#     load_fips_meta()
#     counter = 0
#     for fips in FIPS.msa_fips:
#         post_msa_timeseries(fips)
#         counter += 1
#         if counter % 100 == 0:
#             print(counter)
