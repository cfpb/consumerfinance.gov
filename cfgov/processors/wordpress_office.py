import sys
import json
import os.path
import requests
from sheerlike.external_links import process_external_links


def posts_at_url(url):

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

    for post in posts_at_url(url):
        yield process_office(post)


def process_office(post):

    post['_id'] = post['slug']
    custom_fields = post['custom_fields']

    # get intro text & subscribe form data from custom fields
    intro = {}
    for attr in ['intro_text',
                 'intro_subscribe_form',
                 'intro_govdelivery_code']:
        if attr in custom_fields:
            new_attr = attr.replace('intro_', '')
            intro[new_attr] = custom_fields[attr]
    if intro:
        post['intro'] = intro

    # build top story dict
    top_story = {}
    for attr in ['top_story_head', 'top_story_desc']:
        if attr in custom_fields:
            new_attr = attr.replace('top_story_', '')
            top_story[new_attr] = custom_fields[attr]

    # convert top story links into a proper list
    if 'top_story_links' in custom_fields:
        top_story['links'] = custom_fields['top_story_links']
    else:
        top_story_links = []
        for x in range(5):
            key = 'top_story_links_%s' % x
            if key in custom_fields:
                top_story_links.append({'url': custom_fields[key][0],
                                        'label': custom_fields[key][1]})

        if top_story_links:
            top_story['links'] = top_story_links

    if top_story:
        post['top_story'] = top_story

    # create list of office resource dicts
    if 'resources' in custom_fields:
        post['resources'] = custom_fields['resources']
    else:
        post['resources'] = []
        for x in range(4):
            resource = {}
            fields = ['title', 'desc', 'icon', 'link']
            for field in fields:
                field_name = 'resource_%s_%s' % (str(x), field)
                if field_name in custom_fields and custom_fields[field_name]:
                    if field == 'link':
                        resource[field] = \
                            {'url': custom_fields[field_name][0],
                             'label': custom_fields[field_name][1]}
                    else:
                        resource[field] = custom_fields[field_name]

            if resource:
                post['resources'].append(resource)

    # add other custom fields
    names = ['og_title', 'og_image', 'og_desc', 'twtr_text', 'twtr_lang',
             'twtr_rel', 'twtr_hash', 'utm_campaign', 'utm_term',
             'utm_content', 'short_title', 'related_sub_pages']
    for name in names:
        if name in custom_fields:
            post[name] = custom_fields[name]

    for related in ['related_hero', 'related_contact', 'related_faq']:
        if related in custom_fields:
            if isinstance(custom_fields[related], basestring):
                post[related] = custom_fields[related]
            else:
                post[related] = custom_fields[related][0]

    post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]
    for i, tag in enumerate(post['tags']):
        if not tag.isalnum():
            for char in tag:
                if (not char.isalnum()
                        and not char.isspace()
                        and not char == '-'):
                    post['tags'][i] = tag.replace(char, '')

    del post['custom_fields']

    post = process_external_links(post)

    return {'_type': 'office',
            '_id': post['slug'],
            '_source': post}
