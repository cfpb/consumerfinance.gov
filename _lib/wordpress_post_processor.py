import sys
import json
import os.path
import requests
import dateutil.parser


def posts_at_url(url):

    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:

        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page, 'count': '-1'})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']
        total = 0
        for p in results['posts']:
            total += 1
            yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_post(post)


def process_post(post):
    del post['comments']
    post['_id'] = post['slug']
    # Set the proper keys for Newsroom
    if post['type'] == 'cfpb_newsroom':
        post['category'] = [cat['title'].replace('&amp;', '&')
                            for cat in
                            post['taxonomy_cfpb_newsroom_cat_taxonomy']]
        post['author'] = [author['title'] for author in
                          post['taxonomy_fj_author'] if 'Press Release' not in
                          post['category']]
    # Set the proper keys for Blog
    elif post['type'] == 'post':
        post['blog_category'] = [cat['title'].replace('&amp;', '&') for cat in
                                 post['taxonomy_fj_category']]
        post['category'] = ['Blog']
        post['author'] = [author['title'] for author in
                          post['taxonomy_fj_author']]
    # Set the proper keys for Featured Topic
    if post['type'] == 'featured_topic':
        post['author'] = [post['author']['name']]
        # convert featured_topic_data_x into a proper list
        links = []
        for x in xrange(0, 10):
            custom_fields = post['custom_fields']
            key = 'featured_topic_data_%s_link' % x
            if key in custom_fields:
                links.append(custom_fields[key])
        post['links'] = links
    else:
        post['tags'] = [tag['title'] for tag in post['taxonomy_fj_tag']]

    dt = dateutil.parser.parse(post['date'])
    dt_string = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    post['date'] = dt_string
    if 'twtr_text' in post['custom_fields']:
        post['twtr_text'] = post['custom_fields']['twtr_text'][0]
    if 'twtr_lang' in post['custom_fields']:
        post['twtr_lang'] = post['custom_fields']['twtr_lang'][0]
    if 'twtr_rel' in post['custom_fields']:
        post['twtr_rel'] = post['custom_fields']['twtr_rel'][0]
    if 'twtr_hash' in post['custom_fields']:
        post['twtr_hash'] = post['custom_fields']['twtr_hash'][0]
    return post
