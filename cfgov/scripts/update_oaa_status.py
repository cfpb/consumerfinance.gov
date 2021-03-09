import csv

from v1.models import DocumentDetailPage
from v1.util.migrations import get_data, set_data


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
        data = get_data(page, 'sidefoot')
        for field in data:
            if field['type'] == 'related_metadata':
                field_content = field['value']['content']
                for block in field_content:
                    if block['value'].get('heading', '') == 'Status':
                        if sByURL.get(url):
                            block['value']['blob'] = sByURL[url]
            break
        set_data(page.specific, 'sidefoot', data)


def run():
    update_oaa()
