from __future__ import unicode_literals

import json
import logging

from data_research.models import MortgageMetaData
from data_research.mortgage_utilities.s3_utils import bake_json_to_s3
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta

logger = logging.getLogger(__name__)

"""
# FIPS entries after loading:

# FIPS.county_fips
{'25003':
   {'name': 'Berkshire County',
    'state': 'MA'}
}

# FIPS.msa_fips
{'38340':
   {'fips': '38340',
    'name': 'Pittsfield, MA',
    'county_list': ['25003']}

# FIPS.state_fips
{'09':
   {'AP': 'Conn.',
    'fips': '09',
    'name': 'Connecticut',
    'abbr': 'CT'}
"""


def update_state_to_geo_meta(geo):
    """
    Assemble dictionaries that map state abbreviations to all counties, metro
    areas and non-metro-areas in a given state, for use in building drop-downs.

    Areas are marked `valid: true` or `valid: false` based on whether they meet
    our display threshold of reporting at least 1,000 open mortgages.

    An MSA entry, delivering metadata for a state's MSA and non-MSA areas,
    will look like this:
    ```json
    {
        "HI": {
            "metros": [
                {
                    "fips": "27980",
                    "name": "Kahului-Wailuku-Lahaina, HI",
                    "valid": false
                },
                {
                    "fips": "46520",
                    "name": "Urban Honolulu, HI",
                    "valid": true
                },
                {
                    "fips": "15-non",
                    "valid": true,
                    "name": "Hawaii non-metro area"
                },
            "state_fips": "15",
            "state_name": "Hawaii"
        },
    ...
    }
    ```

    A county meta entry, showing all counties in a state, will look like this:
    ```json
    {
        "DE": {
            "counties": [
                {
                    "fips": "10001",
                    "name": "Kent County"
                    "valid": true,
                },
                {
                    "fips": "10003",
                    "name": "New Castle County"
                    "valid": true,
                },
                {
                    "fips": "10005",
                    "name": "Sussex County"
                    "valid": true,
                }
            ],
            "state_fips": "10",
            "state_name": "Delaware"
        },
    ...
    }
    ```
    """
    non_msa_fips_output = []
    geo_dict = {
        'county': {'label': 'counties',
                   'output_slug': 'state_county_meta',
                   'fips_dict': FIPS.county_fips,
                   'query': MortgageMetaData.objects.get_or_create(
                       name='state_county_meta')},
        'msa': {'label': 'metros',
                'output_slug': 'state_msa_meta',
                'fips_dict': FIPS.msa_fips,
                'query': MortgageMetaData.objects.get_or_create(
                    name='state_msa_meta')}
    }
    g_dict = geo_dict[geo]
    fips_dict = g_dict['fips_dict']
    label = g_dict['label']
    setup = {
        FIPS.state_fips[fips]['abbr']: {
            label: [],
            'state_fips': fips,
            'state_name': FIPS.state_fips[fips]['name']}
        for fips in FIPS.state_fips
    }
    for fips in fips_dict:
        _dict = fips_dict[fips]
        geo_name = _dict['name']
        geo_valid = fips in FIPS.whitelist
        if geo == 'msa':
            msa_state_list = []
            for county_fips in _dict['county_list']:
                state = FIPS.county_fips[county_fips]['state']
                if state not in msa_state_list:
                    msa_state_list.append(state)
            for state_abbr in msa_state_list:
                setup[state_abbr]['metros'].append(
                    {'name': geo_name,
                     'fips': fips,
                     'valid': geo_valid})
        else:  # geo is 'county'
            this_state = FIPS.county_fips[fips]['state']
            setup[this_state]['counties'].append(
                {'name': geo_name,
                 'fips': fips,
                 'valid': geo_valid})
            for state_abbr in setup:
                setup[state_abbr][label].sort(
                    key=lambda entry: entry['fips'])
    if geo == 'msa':
        for state_fips in FIPS.state_fips:
            non_fips = '{}-non'.format(state_fips)
            s_dict = FIPS.state_fips[state_fips]
            state_abbr = s_dict['abbr']
            state_name = s_dict['name']
            non_fips_name = "Non-metro area of {}".format(state_name)
            non_valid = non_fips in FIPS.whitelist
            setup[state_abbr]['metros'].append(
                {'fips': non_fips,
                 'valid': non_valid,
                 'name': "Non-metro area of {}".format(state_name)})
            non_msa_fips_output.append(
                {'fips': non_fips,
                 'valid': non_valid,
                 'name': non_fips_name,
                 'state_name': state_name,
                 'abbr': state_abbr})
    json_out = json.dumps(setup)
    # dump to s3 and save to database
    slug = geo_dict[geo]['output_slug']
    bake_json_to_s3(
        slug,
        json_out,
        sub_bucket='data/mortgage-performance/meta')
    logger.info("Saved '{}.json' to S3".format(slug))
    meta_obj, cr = MortgageMetaData.objects.get_or_create(
        name=slug)
    meta_obj.json_value = setup
    meta_obj.save()
    logger.info("Saved metadata object '{}.'".format(slug))
    if non_msa_fips_output:
        non_meta_obj, cr = MortgageMetaData.objects.get_or_create(
            name='non_msa_fips')
        non_meta_obj.json_value = non_msa_fips_output
        non_meta_obj.save()
        logger.info("Saved non_msa_fips")


def run():
    load_fips_meta()
    for geo in ['msa', 'county']:
        update_state_to_geo_meta(geo)
