import sys
import json
import os.path
import requests
from sheerlike.external_links import process_external_links

import dateutil.parser
import datetime
from pytz import timezone


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint
    count = 20000

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page, 'count': str(count)})
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
    dt_start = dateutil.parser.parse(event['dtstart'])

    # TODO: The times passed in are correct & in ET, 
    # but we want to treat them like we're treating the incorrect times 
    # in our db so that the fix for that is consistent. We can fix this 
    # when Wagtail fixes https://github.com/torchbox/wagtail/issues/2406
    # along with https://github.com/cfpb/cfgov-refresh/pull/1661
    dt_start = dt_start.astimezone(timezone('America/New_York'))
    event['date'] = dt_start.strftime('%Y-%m-%d %H:%M')
    event['dtstart'] = event['date']

    dt_end = dateutil.parser.parse(event['dtend'])
    dt_end = dt_end.astimezone(timezone('America/New_York'))
    event['dtend'] = dt_end.strftime('%Y-%m-%d %H:%M')

    event['day'] = datetime.date(dt_start.year, dt_start.month, dt_start.day)
    if event['description']:
        if event['description'].strip() == '':
            del event['description']
        else:
            event['description'] = event['description'].strip()

    event = process_external_links(event)

    return {'_type': 'calendar_event',
            '_id': event['id'],
            '_source': event}
