import csv
import datetime

from django.http import HttpResponse

from bs4 import BeautifulSoup

from v1.models.enforcement_action_page import EnforcementActionPage


HEADINGS = [
    'Title',
    'Content',
    'Forum',
    'Docket Numbers',
    'Initial Filing Date',
    'Statuses',
    'Products',
    'URL'
]


def assemble_output():
    rows = []
    for page in EnforcementActionPage.objects.all():
        if not page.live:
            continue
        url = 'https://consumerfinance.gov' + page.get_url()
        if 'enforcement/actions' not in url:
            continue
        page_categories = ','.join(
            c.get_name_display() for c in page.categories.all())
        content = ''
        soup = BeautifulSoup(str(page.content), 'html.parser')
        para = soup.findAll(['p', 'h5'])
        for p in para:
            content += p.get_text()
            link = p.find('a', href=True)
            if link:
                content += ': '
                content += link['href']
            content += '\n'
        row = {
            'Title': page.title,
            'Content': content,
            'Forum': page_categories,
            'Docket Numbers': ','.join(
                d.docket_number for d in page.docket_numbers.all()),
            'Initial Filing Date': page.initial_filing_date,
            'Statuses': ','.join(
                d.status for d in page.statuses.all()),
            'Products': ','.join(
                d.product for d in page.products.all()),
            'URL': url
        }
        rows.append(row)

    return rows


def export_actions(path='/tmp', http_response=False):
    """
    A script for exporting Enforcement Actions content
    to a CSV that can be opened easily in Excel.

    Run from within consumerfinance.gov with:
    `python cfgov/manage.py runscript export_enforcement_actions`

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
    with open(file_path, 'w', encoding='utf-8') as f:
        write_questions_to_csv(f)


def write_questions_to_csv(csvfile):
    writer = csv.writer(csvfile)
    writer.writerow(HEADINGS)
    for row in assemble_output():
        writer.writerow([row.get(key) for key in HEADINGS])


def run(*args):
    if args:
        export_actions(path=args[0])
    else:
        export_actions()
