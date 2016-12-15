import json
import os.path
import sys

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
        total = 0
        for p in results['posts']:
            total += 1
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_post(post)


def process_post(post):
    post['_id'] = post['slug']
    post['author'] = [post['author']['name']]
    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'links']
    for name in names:
        if name in post['custom_fields']:
            post[name] = post['custom_fields'][name]
    if 'links' not in post['custom_fields']:
        links = []
        for x in range(10):
            key = 'links_%s' % x
            if key in post['custom_fields']:
                if isinstance(post['custom_fields'][key], basestring):
                    links.append({'url': post['custom_fields'][key]})
                else:
                    links.append({'url': post['custom_fields'][key][0],
                                  'label': post['custom_fields'][key][1]})
        post['links'] = links

    del post['custom_fields']

    post = process_external_links(post)

    return {'_type': 'featured_topic',
            '_id': post['slug'],
            '_source': post}
