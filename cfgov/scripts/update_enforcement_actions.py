from __future__ import unicode_literals

import datetime
import re
from six.moves import html_parser as HTMLParser

from django.http import HttpResponse
from django.utils import html

import unicodecsv

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data


html_parser = HTMLParser.HTMLParser()


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():
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
                        print(clean_and_strip(block['value'].get('heading', '')))
            break
        break


def run():
    assemble_output()
