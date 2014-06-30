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

        resp = requests.get(url, params={'json':1,'page':current_page})
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
    hero_id = post['custom_fields']['related_hero'][0]
    hero_url = os.path.expandvars("$wordpress/hero/" + hero_id + "/?json=1")
    response = requests.get(hero_url)
    hero_data = json.loads(response.text)
    hero_data = hero_data['post']
    related_post_url = os.path.expandvars("$wordpress/api/get_post/?post_slug=" + hero_data['custom_fields']['related_post'][0])
    related_post_response = requests.get(related_post_url)
    hero_data['related_post'] = process_post(json.loads(related_post_response.text)['post'])
    post['hero'] = hero_data

    return post
