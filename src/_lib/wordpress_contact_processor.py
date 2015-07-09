import sys
import json
import os.path
import requests


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']
        total = 0
        for p in results['posts']:
            total += 1
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_contact(post)


def process_contact(contact):
    del contact['comments']
    contact['_id'] = contact['slug']

    names = ['email', 'phone', 'fax']
    for name in names:
        if name in contact['custom_fields']:
            contact[name] = contact['custom_fields'][name]
        else:
            if name is 'fax':
                contact[name] = {}
                if 'fax_num' in contact['custom_fields']:
                    contact[name]['num'] = \
                        contact['custom_fields']['fax_num']
                if 'fax_desc' in contact['custom_fields']:
                    contact[name]['desc'] = \
                        contact['custom_fields']['fax_desc']
                if not contact[name]:
                    del contact[name]
            else:
                contact[name] = []
                for i in range(3):
                    contact[name].append({})
                    if '%s_%s_addr' % (name, i) in contact['custom_fields']:
                        contact[name][i]['addr'] = \
                            contact['custom_fields']['%s_%s_addr' % (name, i)]
                    elif '%s_%s_num' % (name, i) in contact['custom_fields']:
                        contact[name][i]['num'] = \
                            contact['custom_fields']['%s_%s_num' % (name, i)]
                    if '%s_%s_desc' % (name, i) in contact['custom_fields']:
                        contact[name][i]['desc'] = \
                            contact['custom_fields']['%s_%s_desc' % (name, i)]
                    if not contact[name][-1]:
                        contact[name].pop()
    names = ['sitewide_desc', 'attn', 'street', 'city', 'state', 'zip_code',
             'addr_desc']
    for name in names:
        if name in contact['custom_fields']:
            contact[name] = contact['custom_fields'][name]

    if 'web' and 'web_0' in contact['custom_fields']:
        del contact['custom_fields']['web_0']
    elif 'web_0' in contact['custom_fields']:
        contact['custom_fields']['web'] = contact['custom_fields']['web_0']
    if 'web' in contact['custom_fields']:
        if 'url' not in contact['custom_fields']['web'] or \
                'label' not in contact['custom_fields']['web']:
            contact['web'] = {}
            contact['web']['url'] = contact['custom_fields']['web']
        else:
            contact['web'] = contact['custom_fields']['web']

    del contact['custom_fields']

    return {'_type': 'contact',
            '_id': contact['slug'],
            '_source': contact}
