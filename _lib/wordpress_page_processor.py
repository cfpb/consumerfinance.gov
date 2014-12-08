import sys
import json
import os.path
import requests
import dateutil.parser
from string import Template


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:
        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page':current_page, 'count': '-1'})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']

        for p in results['posts']:
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_post(post)


def process_post(post):
    
    del post['comments']
    post['_id'] = post['id']

    # Format date
    dt = dateutil.parser.parse(post['date'])
    dt_string = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    post['date'] = dt_string

    return post
