import sys
import json
import os.path
import requests
from sheerlike.external_links import process_external_links


def posts_at_url(url):

    url = os.path.expandvars(url)
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        resp = requests.get(url, params={'page': current_page})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']
        for p in results['posts']:
            yield p


def documents(name, url, **kwargs):

    for view in posts_at_url(url):
        yield process_view(view)


def process_view(post):
    post['_id'] = post['slug']
    custom_fields = post['custom_fields']

    # limit popular posts to five items
    if 'popular_posts' in custom_fields:
        if isinstance(custom_fields['popular_posts'], basestring):
            post['popular_posts'] = [custom_fields['popular_posts']]
        else:
            popular_posts = [slug for slug in
                             custom_fields['popular_posts'][:5]]
            post['popular_posts'] = popular_posts

    # convert related links into a proper list
    if 'related_links' in post['custom_fields']:
        post['related_links'] = post['custom_fields']['related_links']
    else:
        related = []
        for x in range(5):
            key = 'related_links_%s' % x
            if key in custom_fields:
                if isinstance(custom_fields[key], basestring):
                    related.append({'url': post['custom_fields'][key]})
                else:
                    related.append({'url': post['custom_fields'][key][0],
                                    'label': post['custom_fields'][key][1]})
        post['related_links'] = related

    # append the hero information
    if 'related_hero' in custom_fields:
        if isinstance(custom_fields['related_hero'], basestring):
            hero_id = custom_fields['related_hero']
        else:
            hero_id = custom_fields['related_hero'][0]
        if hero_id:
            hero_url = os.path.expandvars(
                '$WORDPRESS/hero/' + hero_id + '/?json=1')
            response = requests.get(hero_url)
            hero_data = json.loads(response.content)
            if hero_data['status'] is 'ok':
                hero_data = hero_data['post']
                if 'related_post' in hero_data['custom_fields']:
                    hero_data['related_posts'] = \
                        [p for p in hero_data['custom_fields']['related_post']
                         if p]
                post['hero'] = hero_data

    # convert other custom fields
    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'alt_title']
    for name in names:
        if name in post['custom_fields']:
            post[name] = post['custom_fields'][name]

    del post['custom_fields']

    post = process_external_links(post)

    return {'_type': 'views',
            '_id': post['slug'],
            '_source': post}
