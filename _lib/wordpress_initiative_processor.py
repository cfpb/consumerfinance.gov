import sys
import json
import os.path
import requests


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
        yield process_initiative(post)


def process_initiative(item):

    del item['comments']
    item['_id'] = item['slug']
    custom_fields = item['custom_fields']

    if custom_fields.get('related_office'):
        item['related_office'] = custom_fields['related_office'][0]

    # create list of initiative subinitiative dicts
    related = []
    for x in xrange(0, 5):
        key = 'related_link_%s' % x
        if key in custom_fields:
            related.append(custom_fields[key])
    if related:
        item['related_links'] = related

    del item['custom_fields']

    if item['parent'] != 0:
        item['has_parent'] = True
    else:
        item['has_parent'] = False

    return item
