from __future__ import unicode_literals

import json
import logging

from data_research.models import MortgageMetaData
from data_research.mortgage_utilities.s3_utils import bake_json_to_s3
from data_research.views import FIPS, load_fips_meta

logger = logging.getLogger(__name__)

"""
# FIPS entries after loading:

# FIPS.county_fips
{'25003':
   {'name':
    'Berkshire County',
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


def update_state_msa_dropdown():
    """
    Assemble a dictionary that maps state abbreviations to all the metro areas
    in the given state, for use in building MSA drop-downs by state.

    MSAs are marked `valid: true` or `valid: false` based on whether they meet
    our display threshold of reporting at least 1,000 open mortgages.

    A state entry will look like this:
    {
        HI: {
            msas: {
                27980: {
                    valid: false,
                    fips: "27980",
                    name: "Kahului-Wailuku-Lahaina, HI"
                },
                46520: {
                    valid: true,
                    fips: "46520",
                    name: "Urban Honolulu, HI"
                }
            },
            state_fips: "15",
            state_name: "Hawaii"
        },
    ...
    }
    """
    load_fips_meta()
    state_msa_breakdown = {
        FIPS.state_fips[fips]['abbr']: {
            'msas': {},
            'state_fips': fips,
            'state_name': FIPS.state_fips[fips]['name']}
        for fips in FIPS.state_fips
    }
    for msa_fips in FIPS.msa_fips:
        _dict = FIPS.msa_fips[msa_fips]
        msa_name = _dict['name']
        msa_valid = msa_fips in FIPS.whitelist
        state_list = []
        for county_fips in _dict['county_list']:
            state = FIPS.county_fips[county_fips]['state']
            if state not in state_list:
                state_list.append(state)
        for state_abbr in state_list:
            state_msa_breakdown[state_abbr]['msas'].update(
                {msa_fips: {'name': msa_name,
                            'fips': msa_fips,
                            'valid': msa_valid}})
    json_out = json.dumps(state_msa_breakdown)
    # dump to s3 and save to database
    bake_json_to_s3(
        'state_msa_dropdown',
        json_out,
        sub_bucket='data/mortgage-performance/meta')
    logger.info("Saved 'state_msa_dropdown.json' to S3")
    meta_obj, cr = MortgageMetaData.objects.get_or_create(
        name='state_msa_dropdown')
    meta_obj.json_value = json_out
    meta_obj.save()
    logger.info("Saved metadata object 'state_msa_dropdown.'")


def run():
    update_state_msa_dropdown()
