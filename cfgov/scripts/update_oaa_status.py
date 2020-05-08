import csv

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data, set_stream_data


sByURL = {}


def update_oaa():
    with open('./cfgov/scripts/status.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            sByURL[row[0]] = row[1]

    for page in DocumentDetailPage.objects.all():
        if not page.live:
            continue
        url = 'https://www.consumerfinance.gov' + page.get_url()
        if 'administrative-adjudication-docket' not in url:
            continue
        stream_data = get_stream_data(page, 'sidefoot')
        for field in stream_data:
            if field['type'] == 'related_metadata':
                field_content = field['value']['content']
                for block in field_content:
                    if block['value'].get('heading', '') == 'Status':
                        if sByURL.get(url):
                            block['value']['blob'] = sByURL[url]
            break
        set_stream_data(page.specific, 'sidefoot', stream_data)


def run():
    update_oaa()
