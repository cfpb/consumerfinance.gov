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
    
    # get top story & intro text from custom fields
    for attr in ['intro_text', 'intro_subscribe_form', 'top_story_head', 'top_story_desc']:
        if attr in custom_fields:
            item[attr] = custom_fields[attr][0]
    
    # convert top story links into a proper list
    story_links = []
    for x in xrange(0,5):
      key = 'top_story_links_%s' % x
      if key in custom_fields:
          story_links.append(custom_fields[key])
    item['top_story_links'] = story_links
    
    # create list of office resource dicts
    item['resources'] = []
    for x in xrange(1,4):
        resource = {}
        fields = ['head', 'desc', 'icon', 'link_0']
        for field in fields:
            field_name = 'resource%s_%s' % (str(x), field)
            if field_name in custom_fields and custom_fields[field_name][0] != '':
                if field == 'link_0':
                    resource['link'] = custom_fields[field_name]
                else:
                    resource[field] = custom_fields[field_name][0]
                            
        if resource:
            item['resources'].append(resource)
    
    return item