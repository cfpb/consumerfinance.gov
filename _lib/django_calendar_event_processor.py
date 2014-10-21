import sys
import json
import os.path
import requests

def posts_at_url(url):
    
    current_page = 1
    max_page = sys.maxint
    count = 20000

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page':current_page, 'count': str(count)})
        results = json.loads(resp.content) 
        current_page += 1
        max_page = int(results['count']) / count + 1
        for p in results['results']:
            yield p
     
def documents(name, url, **kwargs):
    
    for event in posts_at_url(url):
        yield process_event(event)

def process_event(event):
    event['_id'] = event['id']
    event['urlcal'] = event['calendar'].replace(' ', '').lower()
    return event
