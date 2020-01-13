from __future__ import unicode_literals

import datetime
import html.parser as HTMLParser
import re

from django.http import HttpResponse
from django.utils import html

import unicodecsv

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'Matter name',
    'Date filed',
    'URL',
    'Status',
    'Category',
    'File number',
    'Content',
    'Preview text'
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():
    strip_tags = re.compile(r'<[^<]+?>')
    rows = []
    for page in DocumentDetailPage.objects.all():
        if not page.live:
            continue
        url = 'https://consumerfinance.gov' + page.get_url()
        if 'policy-compliance/enforcement/actions' not in url:
            continue
        page_categories = ','.join(
            c.get_name_display() for c in page.categories.all())
        row = {
            'Matter name': page.title,
            'URL': url,
            'Category': page_categories,
            'Preview text': clean_and_strip(page.preview_description)
        }
        stream_data = get_stream_data(page, 'sidefoot')
        for field in stream_data:
            if field['type'] == 'related_metadata':
                field_content = field['value']['content']
                for block in field_content:
                    if block['value'].get('heading', '') == 'Date filed':
                        row['Date filed'] = str(block['value'].get('date'))
                    elif block['value'].get('heading', '') == 'Status':
                        row['Status'] = strip_tags.sub(
                            '', block['value'].get('blob', ''))
                    elif block['value'].get('heading', '') == 'File number':
                        row['File number'] = strip_tags.sub(
                            '', block['value'].get('blob', ''))
        stream_data_content = get_stream_data(page, 'content')
        for field in stream_data_content:
            if field['type'] == 'full_width_text':
                field_full_width_text = field['value']
                for block in field_full_width_text:
                    if block['type'] == 'content':
                        row['Content'] = clean_and_strip(block['value'])
        rows.append(row)
    return rows


def export_actions(path='/tmp', http_response=False):
    """
    A script for exporting Enforcement Actions content
    to a CSV that can be opened easily in Excel.

    Run from within cfgov-refresh with:
    `python cfgov/manage.py runscript export_enforcement_actions`

    CFPB staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. So we throw in the towel and encode the CSV
    with windows-1252.

    By default, the script will dump the file to `/tmp/`,
    unless a path argument is supplied,
    or http_response is set to True (for downloads via the Wagtail admin).
    A command that passes in path would look like this:
    `python cfgov/manage.py runscript export_enforcement_actions
    --script-args [PATH]`
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = 'enforcement-actions-{}.csv'.format(timestamp)
    if http_response:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment;filename={}'.format(slug)
        write_questions_to_csv(response)
        return response
    file_path = '{}/{}'.format(path, slug).replace('//', '/')
    with open(file_path, 'w') as f:
        write_questions_to_csv(f)


def write_questions_to_csv(csvfile):
    writer = unicodecsv.writer(csvfile, encoding='windows-1252')
    writer.writerow(HEADINGS)
    for row in assemble_output():
        writer.writerow([row.get(key) for key in HEADINGS])


def run(*args):
    if args:
        export_actions(path=args[0])
    else:
        export_actions()
