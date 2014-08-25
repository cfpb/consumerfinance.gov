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
    custom_fields = post['custom_fields']
    if 'email' in custom_fields:
        if custom_fields['email'][0] != '':
            post['email'] = custom_fields['email'][0]
        if custom_fields['email'][1] != '':
            post['email_desc'] = custom_fields['email'][1]
    if 'email_2' in custom_fields:
        if custom_fields['email_2'][0] != '':
            post['email_2'] = custom_fields['email_2'][0]
        if custom_fields['email_2'][1] != '':
            post['email_2_desc'] = custom_fields['email_2'][1]
    if 'phone' in custom_fields:
        if custom_fields['phone'][0] != '':
            post['phone'] = custom_fields['phone'][0]
        if custom_fields['phone'][1] != '':
            post['phone_desc'] = custom_fields['phone'][1]
    if 'phone_2' in custom_fields:
        if custom_fields['phone_2'][0] != '':
            post['phone_2'] = custom_fields['phone_2'][0]
        if custom_fields['phone_2'][1] != '':
            post['phone_2_desc'] = custom_fields['phone_2'][1]
    if 'sitewide_desc' in custom_fields:
        post['sitewide_desc'] = custom_fields['sitewide_desc'][0]
    if 'fax' in custom_fields:
        post['fax'] = custom_fields['fax'][0]
    if 'street' in custom_fields:
        post['street'] = custom_fields['street'][0]
    if 'street_2' in custom_fields:
        post['street_2'] = custom_fields['street_2'][0]
    if 'city' in custom_fields:
        post['city'] = custom_fields['city'][0]
    if 'state' in custom_fields:
        post['state'] = custom_fields['state'][0]
    if 'zip_code' in custom_fields:
        post['zip_code'] = custom_fields['zip_code'][0]
    if 'addr_desc' in custom_fields:
        post['addr_desc'] = custom_fields['addr_desc'][0]
    if 'web' in custom_fields:
        if custom_fields['web'][0] and custom_fields['web'][0] != '':
            post['web'] = custom_fields['web'][0]
        if custom_fields['web'][1] and custom_fields['web'][1] != '':
            post['web_desc'] = custom_fields['web'][1]
    return post
