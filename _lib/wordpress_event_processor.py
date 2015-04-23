# -*- coding: utf-8 -*-

import sys
import json
import os.path
import requests
import dateutil.parser


def posts_at_url(url):
    """
    Get WordPress posts as JSON from the given URL.
    """
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

    ## First some helper functions
    format_datetime = lambda d: dateutil.parser.parse(d).strftime('%Y-%m-%dT%H:%M:%SZ')
    get_custom_field = lambda f, d=[]: event['custom_fields'].get(f, d)
    get_custom_field_member = lambda f, i=0, d='': event['custom_fields'].get(f)[i] \
                                                   if len(event['custom_fields'].get(f, [])) > i \
                                                   else d

    # Do some work on default WP fields
    del event['comments']
    event['_id'] = event['slug']
    event['tags'] = [tag['title'] for tag in event['taxonomy_fj_tag']]
    event['date'] = format_datetime(event['date'])
    event['author'] = event['author']['name']

    # Basic Event Fields
    event['title'] = get_custom_field_member('event_information_title')
    event['event_intro'] = get_custom_field_member('event_information_event_intro', d='')
    event['event_desc'] = get_custom_field_member('event_information_event_desc', d='')

    # Venue Fields
    event['venue'] = {}
    event['venue']['name'] = get_custom_field_member('event_information_venue_name', d='')
    event['venue']['address'] = {}
    event['venue']['address']['address'] = get_custom_field_member('event_information_venue_address_address', d='')
    event['venue']['address']['suite'] = get_custom_field_member('event_information_venue_address_suite', d='')
    event['venue']['address']['city'] = get_custom_field_member('event_information_venue_address_city', d='')
    event['venue']['address']['state'] = get_custom_field_member('event_information_venue_address_state', d='')
    event['venue']['address']['zip_code'] = get_custom_field_member('event_information_venue_address_zip_code', d='')

    # Agenda Fields
    event['agenda'] = {}
    event['agenda']['speaker'] = get_custom_field_member('event_agenda_speaker', d='')
    event['agenda']['desc'] = get_custom_field_member('event_agenda_desc', d='')
    event['agenda']['venue_location'] = get_custom_field_member('event_agenda_venue_location', d='')

    # Timestamps
    event['timestamps'] = {}
    event['timestamps']['event_date'] = get_custom_field_member('event_date')
    event['timestamps']['event_time'] = get_custom_field_member('event_time')
    event['timestamps']['agenda_beginning'] = get_custom_field_member('event_agenda_beginning_time')
    event['timestamps']['agenda_ending'] = get_custom_field_member('event_agenda_ending_time')
    event['timestamps']['published_date'] = get_custom_field_member('event_information_published_date')
    event['timestamps']['post_event'] = get_custom_field_member('become_post_event')
    event['timestamps']['become_live'] = get_custom_field_member('become_live_event')

    # Livestream
    event['livestream'] = {}
    event['livestream']['available'] = get_custom_field_member('live_event_live_stream_available', d='')

    # Post-Event
    event['post_event'] = {}
    event['post_event']['video_transcript'] = get_custom_field_member('post_event_video_transcript', d='')
    event['post_event']['speech_transcript'] = get_custom_field_member('post_event_speech_transcript', d='')
    event['post_event']['flickr_url'] = get_custom_field_member('post_event_flickr_url', d='')
    event['post_event']['youtube_url'] = get_custom_field_member('post_event_youtube_url', d='')

    # Images
    event['images'] = {}
    event['images']['live_event_preview'] = get_custom_field_member('live_event_preview_image')
    event['images']['live_event'] = get_custom_field_member('live_event_live_event_image')
    event['images']['pre-event'] = get_custom_field_member('event_information_pre-event_image')
    event['images']['event'] = get_custom_field_member('event_information_event_image')
    event['images']['post_event_pre'] = get_custom_field_member('post_event_pre-image')
    event['images']['post_event'] = get_custom_field_member('post_event_image')

    # Reservations
    event['reservation'] = {}
    event['reservation']['desc'] = get_custom_field_member('event_information_reservation_desc', d='')
    event['reservation']['contact_info'] = get_custom_field_member('event_information_reservation_contact_info', d='')

    return event

