import sys
import json
import os.path
import requests
import dateutil.parser


def posts_at_url(url):
    
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:
        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page':current_page, 'count': '-1'})
        results = json.loads(resp.content) 
        current_page += 1
        max_page = results['pages']
        for p in results['posts']:
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_history(post)


def process_history(item):

    del item['comments']
    item['_id'] = item['slug']

    if item['parent'] != 0:
        # This is an individual history point
        item['has_parent'] = True
        if item['custom_fields'].get('item_date'):
            item['item_date'] = item['custom_fields']['item_date'][0]
    else:
        # This is history section
        item['has_parent'] = False
        if item['custom_fields'].get('section_date_from'):
            item['section_date_from'] = \
                item['custom_fields']['section_date_from'][0]
        if item['custom_fields'].get('section_date_to'):
            item['section_date_to'] = \
                item['custom_fields']['section_date_to'][0]

    dt = dateutil.parser.parse(item['date'])
    dt_string = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    item['date'] = dt_string

    return item
