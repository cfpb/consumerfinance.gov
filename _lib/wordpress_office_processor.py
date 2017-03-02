import sys
import json
import os.path
import requests

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
        yield process_office(post)


def process_office(item):
    
    item['_id'] = item['slug']
    custom_fields = item['custom_fields']
    
    # get intro text & subscribe form data from custom fields
    for attr in ['intro_text', 'intro_subscribe_form', 'intro_govdelivery_code', 'related_contact']:
        if attr in custom_fields:
            item[attr] = custom_fields[attr][0]
    
    # build top story dict
    top_story = {}
    for attr in ['top_story_head', 'top_story_desc']:
        if attr in custom_fields:
            top_story[attr] = custom_fields[attr][0]
    
    # convert top story links into a proper list
    top_story_links = []
    for x in xrange(0,5):
      key = 'top_story_links_%s' % x
      if key in custom_fields:
          top_story_links.append(custom_fields[key])
          
    if top_story_links:     
        top_story['top_story_links'] = top_story_links
        
    if top_story:
        item['top_story'] = top_story
    
    # create list of office resource dicts
    item['resources'] = []
    for x in xrange(0,4):
        resource = {}
        fields = ['head', 'desc', 'icon', 'link']
        for field in fields:
            field_name = 'resource_%s_%s' % (str(x), field)
            if field_name in custom_fields and custom_fields[field_name][0] != '':
                if field == 'link':
                    resource[field] = custom_fields[field_name]
                else:
                    resource[field] = custom_fields[field_name][0]
                    
        if resource:
            item['resources'].append(resource)

    return item

