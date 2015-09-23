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
    post['blog_category'] = [cat['title'].replace('&amp;', '&') for cat in
                             post['taxonomy_fj_category']]
    post['category'] = ['Blog']
    post['author'] = [author['title'] for author in
                      post['taxonomy_fj_author']]
    post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]

    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'alt_title', 'popular_posts',
             'show_featured_image_in_post', 'display_in_newsroom',
             'related_links', 'dsq_needs_sync', 'dsq_thread_id']
    for name in names:
        if name in post['custom_fields']:
            post[name] = post['custom_fields'][name]

    if 'related_hero' in post['custom_fields']:
        if isinstance(post['custom_fields']['related_hero'], basestring):
            post['related_hero'] = post['custom_fields']['related_hero']
        else:
            post['related_hero'] = post['custom_fields']['related_hero'][0]

    if 'related_links' not in post:
        related = []
        for x in range(5):
            key = 'related_links_%s' % x
            if key in post['custom_fields']:
                related.append({'url': post['custom_fields'][key][0],
                                'label': post['custom_fields'][key][1]})
        post['related_links'] = related

    del post['custom_fields']

    return {'_type': 'posts',
            '_id': post['slug'],
            '_source': post}
