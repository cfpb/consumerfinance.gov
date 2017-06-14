from __future__ import absolute_import, unicode_literals

import requests

from six import print_


HUD_COUNSELORS_URL = (
    'https://data.hud.gov/Housing_Counselor/searchByLocation?'
    'Lat=38.8951&Long=-77.0367&Distance=5000'
)

HUD_LANGUAGES_URL = 'https://data.hud.gov/Housing_Counselor/getLanguages'

HUD_SERVICES_URL = 'https://data.hud.gov/Housing_Counselor/getServices'


def fetch_counselors():
    """Download housing counselor data from HUD.

    This class fetches housing counselor data from data.hud.gov and also
    expands any language and service abbreviations contained within.
    """
    counselors = download_housing_counselors(HUD_COUNSELORS_URL)

    for key, url in (
        ('languages', HUD_LANGUAGES_URL),
        ('services', HUD_SERVICES_URL),
    ):
        replace_abbreviations(counselors, key, url)

    return counselors


def download_housing_counselors(url):
    """Download HUD counselors from a given URL."""
    print_('Downloading HUD counselors from', url, flush=True)
    counselors = get_json_from_url(url)

    if not counselors:
        raise RuntimeError('Could not download HUD counselors')

    print_('Retrieved', len(counselors), 'counselors', flush=True)
    return counselors


def replace_abbreviations(counselors, attribute, url):
    """Replace attribute abbreviations with names from a given URL."""
    print_('Downloading counselor', attribute, 'from', url, flush=True)
    values = get_json_from_url(url)
    values_dict = dict((lang['key'], lang['value']) for lang in values)

    for counselor in counselors:
        abbreviations = counselor[attribute]
        counselor[attribute] = map(
            lambda key: values_dict[key],
            abbreviations.split(',') if abbreviations else []
        )


def get_json_from_url(url):
    """Retrieve JSON from a URL, raising on failure."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
