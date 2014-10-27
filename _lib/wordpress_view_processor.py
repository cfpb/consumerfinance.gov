import sys
import json
import os.path
from string import Template
from wordpress_post_processor import process_post

import requests

import dateutil.parser

def posts_at_url(url):
    
    url = os.path.expandvars(url)
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        resp = requests.get(url, params={'page':current_page})
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
        popular_posts = [slug for slug in custom_fields['popular_posts'][:5]]
        post['popular_posts'] = popular_posts

    # convert related links into a proper list
    related =[]
    for x in xrange(0,5):
        key = 'related_link_%s' % x
        if key in custom_fields:
            related.append(custom_fields[key])
    post['related_links'] = related

    # append the hero information
    if 'related_hero' in custom_fields and custom_fields['related_hero'][0] != '':
        hero_id = custom_fields['related_hero'][0]
        hero_url = os.path.expandvars("$WORDPRESS/hero/" + hero_id + "/?json=1")
        response = requests.get(hero_url)
        hero_data = json.loads(response.text)
        hero_data = hero_data['post']
        hero_data['related_post'] = hero_data['custom_fields']['related_post'][0]
        post['hero'] = hero_data

    return post
