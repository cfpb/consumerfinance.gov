import sys
import json
import os.path
import requests

import dateutil.parser
import datetime

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
    event['date'] = event['dtstart']
    dt = dateutil.parser.parse(event['dtstart'])
    event['day'] = datetime.date(dt.year, dt.month, dt.day)
    if event['description']:
        if event['description'].strip() == '':
            del event['description']
        else:
            event['description'] = event['description'].strip()
    return event
