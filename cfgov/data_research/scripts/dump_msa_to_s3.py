from __future__ import unicode_literals

import json
import os

import boto
from boto.s3.connection import OrdinaryCallingFormat

from data_research.views import FIPS, load_fips_meta
from data_research.models import MSAMortgageData

S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET')
s3_base = "http://files.consumerfinance.gov"  # not using ssl for s3
keyname = "data/mortgage-performance/metro"


def prep_key(key, content):
    """Prep content for an s3 endpoint 'key'."""
    key.set_contents_from_string(content)
    key.set_acl('public-read')
    key.content_type = 'application/json'
    return key


def bake_msa_to_s3(fips, day_range, json_string):
    from boto.s3.key import Key
    s3 = boto.connect_s3(S3_KEY,
                         S3_SECRET,
                         calling_format=OrdinaryCallingFormat())
    bucket = s3.get_bucket('files.consumerfinance.gov')
    json_prep = Key(
        bucket=bucket, name='{}/{}_{}_day_delinq_percent.json'.format(
            keyname, fips, day_range))
    json_prep = prep_key(json_prep, json_string)


def post_msa_timeseries(fips):
    records = MSAMortgageData.objects.filter(fips=fips)
    name = FIPS.msa_fips[fips]['msa']
    data = {'label': name,
            'data': [record.time_series for record in records]}
    json_string = json.dumps(data)
    day_range = '30'
    bake_msa_to_s3(fips, day_range, json_string)


def run():
    load_fips_meta()
    counter = 0
    for fips in FIPS.msa_fips:
        post_msa_timeseries(fips)
        counter += 1
        if counter % 100 == 0:
            print(counter)
