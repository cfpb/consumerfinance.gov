import logging

from django.conf import settings

import requests


logger = logging.getLogger(__name__)

SEARCH_DOT_GOV_AFFILIATE = settings.SEARCH_DOT_GOV_AFFILIATE
SEARCH_DOT_GOV_ACCESS_KEY = settings.SEARCH_DOT_GOV_ACCESS_KEY


def search(query, limit=20, offset=0,
           enable_highlighting=True, sort_by='relevance'):

    if 1 > limit or limit > 50:
        raise ValueError('limit has to be between 1-50')

    if 0 > offset or offset > 999:
        raise ValueError('offset has to be between 0-999')

    if sort_by not in ('relevance', 'date'):
        raise ValueError('sort_by must be one of relevance or date')

    search_url = 'https://search.usa.gov/api/v2/search/i14y'
    search_params = {
        'query': query,
        'affiliate': SEARCH_DOT_GOV_AFFILIATE,
        'access_key': SEARCH_DOT_GOV_ACCESS_KEY,
        'limit': limit,
        'offset': offset,
        'enable_highlighting': enable_highlighting,
        'sort_by': sort_by
    }

    response = requests.get(search_url, params=search_params)

    if not response.ok:
        logging.error("Got a bad response from search.gov search API")
        return {}

    return response.json()


def typeahead(query):
    typeahead_url = 'https://search.usa.gov/sayt'
    typeahead_params = {
        'q': query,
        'name': SEARCH_DOT_GOV_AFFILIATE,
    }

    response = requests.get(typeahead_url, params=typeahead_params)

    if not response.ok:
        logging.error("Got a bad response from search.gov typeahead API")
        return []

    return response.json()
