import sys
import json
import requests
from string import Template

import dateutil.parser

def posts_at_url(url):
    
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

    # convert related links into a proper list
    related =[]
    for x in xrange(0,5):
        key = 'related_link_%s' % x
        if key in custom_fields:
            related.append(custom_fields[key])
    post['related_links'] = related

    # append the her information
    hero_id = post['custom_fields']['related_hero'][0]
    hero_url = "http://your.wordpress.domain/api/get_post/?post_id=" + hero_id + "&post_type=cfpb_hero"
    response = requests.get(hero_url)
    hero_data = json.loads(response.text)
    post['hero'] = hero_data
    return post