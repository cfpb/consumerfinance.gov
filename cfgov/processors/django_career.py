import json
import os.path
import sys

import requests

from sheerlike.external_links import process_external_links


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint
    count = 20000

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page,
                                         'count': str(count)})
        results = json.loads(resp.content)
        current_page += 1
        max_page = int(results['count']) / count + 1
        for p in results['results']:
            yield p


def documents(name, url, **kwargs):

    for career in posts_at_url(url):
        yield process_career(career)


def process_career(career):
    career['_id'] = career['id']
    for salary in ['salary_' + m for m in ['max', 'min']
                   if career['salary_' + m]]:
        career[salary] = float(career[salary])
    if 'applicant_types' in career:
        for ap_types in career['applicant_types']:
            if 'application_type' in ap_types:
                ap_types['application_type']['name'] = \
                    ap_types['application_type']['applicant_type']
                del ap_types['application_type']['applicant_type']
    career = process_external_links(career)
    return {'_type': 'career',
            '_id': career['id'],
            '_source': career}
