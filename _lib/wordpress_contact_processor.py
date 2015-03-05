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

def convert_custom_field(post_type, attribute, index=0, new_attribute=None):
    # Check to make sure the index is in range for the list
    if attribute in post_type['custom_fields'] and \
        len(post_type['custom_fields'][attribute]) >= (index + 1):
        if new_attribute is None:
            post_type[attribute] = post_type['custom_fields'][attribute][index]
        else:
            post_type[new_attribute] = post_type['custom_fields'][attribute][index]

def process_contact(contact):
    del contact['comments']
    contact['_id'] = contact['slug']
    convert_custom_field(contact, 'email_addr')
    convert_custom_field(contact, 'email_desc')
    convert_custom_field(contact, 'email_2_addr')
    convert_custom_field(contact, 'email_2_desc')
    convert_custom_field(contact, 'phone_num')
    convert_custom_field(contact, 'phone_desc')
    convert_custom_field(contact, 'phone_2_num')
    convert_custom_field(contact, 'phone_2_desc')
    convert_custom_field(contact, 'fax_num')
    convert_custom_field(contact, 'fax_desc')
    convert_custom_field(contact, 'sitewide_desc')
    convert_custom_field(contact, 'attn')
    convert_custom_field(contact, 'street')
    convert_custom_field(contact, 'city')
    convert_custom_field(contact, 'state')
    convert_custom_field(contact, 'zip_code')
    convert_custom_field(contact, 'addr_desc')
    convert_custom_field(contact, 'web_0', index=0, new_attribute='web_addr')
    convert_custom_field(contact, 'web_0', index=1, new_attribute='web_desc')
    return contact
