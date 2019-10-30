from __future__ import unicode_literals

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data
from v1.tests.wagtail_pages.helpers import publish_changes


def update_field_name():
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
                        print(block['value'].get('heading', ''))
                        print(block['value'].get('blob', ''))
            break
        publish_changes(page.specific)
        break


def run():
    update_field_name()
