import sys
import json
import os.path
import requests
from sheerlike.external_links import process_external_links


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page, 'count': '-1'})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']
        for p in results['posts']:
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_orgmember(post)


def process_orgmember(member):
    del member['comments']
    member['_id'] = member['slug']
    if member['parent'] != 0:
        member['has_parent'] = True
    else:
        member['has_parent'] = False
    if member['taxonomy_orgmember_cat']:
        member['category'] = \
            member['taxonomy_orgmember_cat'][0]['title'].replace('&amp;', '&')
    if member['custom_fields'].get('name'):
        member['name'] = member['custom_fields'].get('name')
    else:
        member['name'] = ''
    if member['custom_fields'].get('titles'):
        member['titles'] = member['custom_fields'].get('titles')
    else:
        member['titles'] = [member['custom_fields'].get(title)
                            for title in ['titles_0', 'titles_1']
                            if member['custom_fields'].get(title)]
    del member['custom_fields']

    member = process_external_links(member)

    return {'_type': 'orgmember',
            '_id': member['slug'],
            '_source': member}
