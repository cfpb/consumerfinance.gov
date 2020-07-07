import re

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import pypandoc
from research_reports.models import AuthorNames, Report

report_type_target = 'Report [Tt]ype: '
title_target = 'Title: '
subtitle_target = 'Subtitle: '
authors_target = 'Authors: '
blank = ''


def document_as_beautifulsoup(report_page):
    print(" *** downloading the report file... ***")
    with report_page.report_file.file.file.open() as f:
        raw_report = f.read()

    print(" *** converting the report to html... ***")
    output = pypandoc.convert_text(raw_report, format='docx', to='html')
    return BeautifulSoup(output, 'html.parser')


def targeted_string(target, soup):
    found_string = soup.find(string=re.compile(target))
    if found_string:
        return re.sub(target, blank, found_string)
    else:
        return ''

def authors(soup):
    authors_string = targeted_string(authors_target, soup)
    authors_list = re.split(', ', authors_string)
    return [AuthorNames(name=name) for name in authors_list]

def footnotes(soup):
    return soup.find('section', class_='footnotes')

# def main_content(soup):


def run(report_page):
    soup = document_as_beautifulsoup(report_page)

    print(" *** inserting report data into the page... ***")
    # First page fields
    report_page.report_type = targeted_string(report_type_target, soup)
    report_page.header = targeted_string(title_target, soup)
    report_page.subheader = targeted_string(subtitle_target, soup)
    report_page.report_author_names = authors(soup)

    # Main Content

    # Appendices

    # Footnotes
    report_page.footnotes = footnotes(soup)

    print(" *** saving the page... ***")
    report_page.process_report = False
    report_page.save_revision()  # future: add user= keyword
    report_page.save()


# To invoke this command from the cfgov-refresh root:
#     cfgov/manage.py parse_research_report [report_page_id]
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_page_id', type=int)

    def handle(self, *args, **options):
        report_id = options['report_page_id']
        print('received id as argument: ', id)

        print(" *** finding report page... ***")
        report_page = Report.objects.get(id=report_id)
        run(report_page)
