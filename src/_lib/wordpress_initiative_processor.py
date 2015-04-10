import sys
import json
import os.path
import requests
import dateutil.parser


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
        yield process_initiative(post)


def process_initiative(item):

    del item['comments']
    item['_id'] = item['slug']
    custom_fields = item['custom_fields']

    if custom_fields.get('related_office'):
        item['related_office'] = \
            custom_fields['related_office'][0]
            
    # create list of initiative subinitiative dicts
    item['subinitiatives'] = []
    
    for x in xrange(0,6):
        subinitiative = {}
        fields = ['header', 'desc']
        subinitiative_links = []
        
        for field in fields:
            field_name = 'subinitiative_%s_%s' % (field, str(x))
            if field_name in custom_fields and custom_fields[field_name][0] != '':
                subinitiative[field] = custom_fields[field_name][0]
                
        for y in xrange(0,5):
            link_name = 'subinitiative_links_%s_%s' % (str(x), str(y))
            if link_name in custom_fields:
                subinitiative_links.append(custom_fields[link_name])

        if subinitiative_links:
            subinitiative['links'] = subinitiative_links

        if subinitiative:
            item['subinitiatives'].append(subinitiative)      
    
    return item
