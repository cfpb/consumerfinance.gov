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
        total = 0
        for p in results['posts']:
            total += 1
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_post(post)


def process_post(post):
    del post['comments']
    post['_id'] = post['slug']
    post['category'] = [cat['title'].replace('&amp;', '&')
                        for cat in
                        post['taxonomy_cfpb_newsroom_cat_taxonomy']]
    post['author'] = [author['title'] for author in
                      post['taxonomy_fj_author'] if 'Press Release' not in
                      post['category']]
    post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]

    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'dsq_thread_id', 'alt_title']
    for name in names:
        if name in post['custom_fields']:
            post[name] = post['custom_fields'][name]

    del post['custom_fields']

    return {'_type': 'newsroom',
            '_id': post['slug'],
            '_source': post}
