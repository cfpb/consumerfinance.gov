import sys
import json
import os.path
import requests
from string import Template

import dateutil.parser

def posts_at_url(url):
    
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page':current_page})
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

    # Optionally include additional documents with specific values in custom fields
    if 'supplement' in kwargs:
        supplement = kwargs['supplement']
        for post in posts_at_url(supplement['url']):
            if supplement['field'] in post['custom_fields'] and \
               supplement['expected_value'] in post['custom_fields'][supplement['field']]:
                yield process_post(post)


def process_post(post):
    del post['comments']
    post['_id'] = post['slug']
    # remove fields we're not interested in
    if post['type'] == 'cfpb_newsroom':
        post['category'] = [cat['title'].replace('&amp;', '&') for cat in post['taxonomy_cfpb_newsroom_cat_taxonomy']]
    elif post['type'] == 'post':
        post['category'] = [cat['title'].replace('&amp;', '&') for cat in post['taxonomy_fj_category']]
    if post['type'] == 'watchroom':
        post['author'] = [post['author']['name']]
        # convert watchroom_data_x into a proper list
        links = []
        for x in xrange(0,5):
            custom_fields = post['custom_fields']
            key = 'watchroom_data_%s' % x
            if key in custom_fields:
                links.append(custom_fields[key])
        post['links'] = links
    else:
        post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]
        post['author'] = [author['title'] for author in post['taxonomy_author']]
    author_template = Template("$first_name $last_name")
    dt = dateutil.parser.parse(post['date'])
    dt_string = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    post['date'] = dt_string
    return post
