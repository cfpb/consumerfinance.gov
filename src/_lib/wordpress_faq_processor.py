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
        yield process_post(post)


def process_post(post):

    post['_id'] = post['slug']

    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'faq']
    for name in names:
        if name in post['custom_fields']:
            post[name] = post['custom_fields'][name]
    if 'taxonomy_fj_tag' in post:
        post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]

    del post['custom_fields']

    return {'_type': 'faq',
            '_id': post['slug'],
            '_source': post}
