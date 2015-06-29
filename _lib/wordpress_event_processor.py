# -*- coding: utf-8 -*-

import sys
import json
import os.path
import requests
import dateutil.parser
from collections import OrderedDict


def posts_at_url(url):
    """
    Get WordPress posts as JSON from the given URL.
    """
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:
        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page, 'count': '-1'})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']
        for p in results['posts']:
            yield p


def documents(name, url, **kwargs):
    """
    Yield documents to be indexed in Elasticsearch, one at a time.
    """
    for event in posts_at_url(url):
        yield process_event(event)


def process_event(event):
    """
    Process an event as provided by the WordPress API and return
    JSON suitable for indexing in Elasticsearch.
    """
    del event['comments']
    event['_id'] = event['slug']
    custom_fields = event['custom_fields']

    # Reassign data out of custom fields
    event['tags'] = [tag['title'] for tag in event['taxonomy_fj_tag']
                     if event['taxonomy_fj_tag']]
    event['open_graph'] = {}
    og_fields = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_rel',
                 'twtr_lang', 'twtr_hash', 'utm_campaign', 'utm_term',
                 'utm_content']
    event_fields = ['rsvp', 'agenda', 'venue', 'archive', 'live', 'future',
                    'live_stream']
    for field in og_fields:
        if field in custom_fields and custom_fields[field]:
            event['open_graph'][field] = custom_fields[field]
    for field in event_fields:
        if field in custom_fields and custom_fields[field]:
            event[field] = custom_fields[field]

    if 'taxonomy_beginning_time' in event and event['taxonomy_beginning_time']:
            event['beginning_time'] = \
                event['taxonomy_beginning_time'][0]['title']
    if 'taxonomy_ending_time' in event and event['taxonomy_ending_time']:
            event['ending_time'] = \
                event['taxonomy_ending_time'][0]['title']

    if 'agenda' in event:
        for agenda in event['agenda']:
            if 'beginning_time' in agenda and \
                    'date' in agenda['beginning_time']:
                agenda['beginning_time'] = agenda['beginning_time']['date']
            if 'ending_time' in agenda and 'date' in agenda['ending_time']:
                agenda['ending_time'] = agenda['ending_time']['date']

    if 'live_stream' in event:
        if event['live_stream'] and 'date' in event['live_stream']:
            event['live_stream'] = event['live_stream']['date']

    # Delete taxonomy data and custom fields
    del event['custom_fields']
    for key, value in event.items():
        if key.startswith('taxonomy'):
            del event[key]

    event = OrderedDict(sorted(event.items(), key=lambda k: k[0]))

    return {'_index': 'content',
            '_type': 'events',
            '_id': event['slug'],
            '_source': event}
