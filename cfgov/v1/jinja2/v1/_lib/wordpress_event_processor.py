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
        event['beginning_time'] = {}
        event['beginning_time']['date'] = \
            event['taxonomy_beginning_time'][0]['title']
        event['beginning_time']['timezone'] = \
            event['taxonomy_beginning_time'][0]['description']
    if 'taxonomy_ending_time' in event and event['taxonomy_ending_time']:
        event['ending_time'] = {}
        event['ending_time']['date'] = \
            event['taxonomy_ending_time'][0]['title']
        event['ending_time']['timezone'] = \
            event['taxonomy_ending_time'][0]['description']

    # Create ICS data dictionary
    event['ics'] = {}
    if 'title' in event:
        event['ics']['summary'] = event['title']
    if 'venue' in event:
        if 'city' and 'state' in event['venue']:
            event['ics']['location'] = "%s, %s" % (event['venue']['city'],
                                                   event['venue']['state'])
    if 'beginning_time' in event:
        event['ics']['dtstart'] = event['beginning_time']['date']
        event['ics']['starting_tzinfo'] = event['beginning_time']['timezone']
    if 'ending_time' in event:
        event['ics']['dtend'] = event['ending_time']['date']
        event['ics']['ending_tzinfo'] = event['ending_time']['timezone']
    ics_dict = {'date': 'dtstamp', 'relative_url': 'uid'}
    for wp_field, ics_field in ics_dict.items():
        if wp_field in event and event[wp_field]:
            event['ics'][ics_field] = event[wp_field]

    # Delete taxonomy data and custom fields
    del event['custom_fields']
    for key, value in event.items():
        if key.startswith('taxonomy'):
            del event[key]

    event = OrderedDict(sorted(event.items(), key=lambda k: k[0]))

    return {'_type': 'events',
            '_id': event['slug'],
            '_source': event}
