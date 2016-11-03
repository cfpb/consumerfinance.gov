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
        yield process_sub_page(post)


def process_sub_page(post):

    del post['comments']
    post['_id'] = post['slug']
    custom_fields = post['custom_fields']

    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'show_in_office', 'use_filtered_feed', 'use_form',
             'body_content', 'related_links', 'short_title', 'preview_text']
    for name in names:
        if name in custom_fields:
            post[name] = custom_fields[name]
    if 'related_faq' in custom_fields:
        if isinstance(custom_fields['related_faq'], basestring):
            post['related_faq'] = custom_fields['related_faq']
        else:
            post['related_faq'] = custom_fields['related_faq'][0]
    if 'related_links' not in post:
        related = []
        for x in range(5):
            key = 'related_links_%s' % x
            if key in custom_fields:
                related.append({'url': custom_fields[key][0],
                                'label': custom_fields[key][1]})
        if related:
            post['related_links'] = related
    del post['custom_fields']

    if 'taxonomy_fj_tag' in post:
        post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]
        for i, tag in enumerate(post['tags']):
            if not tag.isalnum():
                for char in tag:
                    if (not char.isalnum()
                            and not char.isspace()
                            and not char == '-'):
                        post['tags'][i] = tag.replace(char, '')

    if post['parent'] != 0:
        post['has_parent'] = True
    else:
        post['has_parent'] = False

    post = process_external_links(post)

    return {'_type': 'sub_page',
            '_id': post['slug'],
            '_source': post}
