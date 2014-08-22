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
        yield process_contact(post)

def process_contact(post):
    del post['comments']
    post['_id'] = post['slug']
    if 'email' in post['custom_fields']:
        post['email'] = post['custom_fields']['email'][0]
        post['email_desc'] = post['custom_fields']['email'][1]
    if 'email_2' in post['custom_fields']:
        post['email_2'] = post['custom_fields']['email_2'][0]
        post['email_2_desc'] = post['custom_fields']['email_2'][1]
    if 'phone' in post['custom_fields']:
        post['phone'] = post['custom_fields']['phone'][0]
        post['phone_desc'] = post['custom_fields']['phone'][1]
    if 'phone_2' in post['custom_fields']:
        post['phone_2'] = post['custom_fields']['phone_2'][0]
        post['phone_2_desc'] = post['custom_fields']['phone_2'][1]
    if 'sitewide_desc' in post['custom_fields']:
        post['sitewide_desc'] = post['custom_fields']['sitewide_desc'][0]
    if 'fax' in post['custom_fields']:
        post['fax'] = post['custom_fields']['fax'][0]
    if 'street' in post['custom_fields']:
        post['street'] = post['custom_fields']['street'][0]
    if 'street_2' in post['custom_fields']:
        post['street_2'] = post['custom_fields']['street_2'][0]
    if 'city' in post['custom_fields']:
        post['city'] = post['custom_fields']['city'][0]
    if 'state' in post['custom_fields']:
        post['state'] = post['custom_fields']['state'][0]
    if 'zip_code' in post['custom_fields']:
        post['zip_code'] = post['custom_fields']['zip_code'][0]
    if 'addr_desc' in post['custom_fields']:
        post['addr_desc'] = post['custom_fields']['addr_desc'][0]
    if 'web' in post['custom_fields']:
        post['web'] = post['custom_fields']['web'][0]
    return post
