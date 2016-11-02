import json
import requests
from sheerlike.external_links import process_external_links


def posts_at_url(url):

    results = {'posts': []}
    for post_id in ['36603', '36605', '36601']:
        resp = requests.get('http://www.consumerfinance.gov/api/get_post/',
                            params={'post_type': 'page', 'post_id': post_id})
        results['posts'].append(json.loads(resp.content)['post'])

    for p in results['posts']:
        yield p


def documents(name, url, **kwargs):

    for post in posts_at_url(url):
        yield process_post(post)


def process_post(page):

    del page['comments']
    page['_id'] = page['id']

    page = process_external_links(page)

    return {'_type': 'pages',
            '_id': page['id'],
            '_source': page}
