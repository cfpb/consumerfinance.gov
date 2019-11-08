from __future__ import unicode_literals
from re import search, IGNORECASE

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data, set_stream_data
from v1.tests.wagtail_pages.helpers import publish_changes

def update_category(current):
    stip = search('Stipulation and consent order', current, IGNORECASE)
    admin = search('Administrative adjudication', current, IGNORECASE)

    if stip or admin:
        return 'Administrative Proceeding'
    elif search('Federal district court case', current, IGNORECASE):
        return 'Civil Action'
    else:
      return current


def update_sidefoot():
    for page in DocumentDetailPage.objects.all():
        if not page.live:
            continue
        url = 'https://consumerfinance.gov' + page.get_url()
        if 'policy-compliance/enforcement/actions' not in url:
            continue
        stream_data = get_stream_data(page, 'sidefoot')
        for field in stream_data:
            if field['type'] == 'related_metadata':
                field_content = field['value']['content']
                for block in field_content:
                    if block['value'].get('heading', '') == 'File number':
                        block['value']['heading'] = 'Docket number'
                    if block['value'].get('heading', '') == 'Category':
                        block['value']['blob'] = update_category(block['value']['blob'])
            break
        set_stream_data(page.specific, 'sidefoot', stream_data)


def run():
    update_sidefoot()
