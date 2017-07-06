from __future__ import unicode_literals

import datetime
import sys

import HTMLParser
from django.utils import html

from ask_cfpb.models import Answer

try:
    from paying_for_college.csvkit import csvkit
except ImportError:
    print("Import error: Try installing college-costs")
    sys.exit(1)


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'SpanishQuestion',
    'SpanishAnswer',
    'SpanishURL',
    'Topic',
    'SubCategories',
    'Audiences',
    'RelatedQuestions',
    'RelatedResources',
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():
    answers = Answer.objects.all()
    output_rows = []
    for answer in answers:
        output = {heading: '' for heading in HEADINGS}
        output['ASK_ID'] = answer.id
        output['Question'] = answer.question
        output['ShortAnswer'] = clean_and_strip(
            answer.snippet)
        output['Answer'] = clean_and_strip(
            answer.answer)
        # output['SpanishAnswer'] = clean_and_strip(
        #     answer.answer_es)
        output['URL'] = answer.english_page.url_path.replace(
            '/cfgov', '') if answer.english_page else ''
        output['SpanishQuestion'] = answer.question_es.replace('\x81', '')
        output['SpanishAnswer'] = clean_and_strip(
            answer.answer_es).replace('\x81', '')
        output['SpanishURL'] = (
            answer.spanish_page.url_path.replace(
                '/cfgov', '') if answer.spanish_page else '')
        output['Topic'] = answer.category.first().name
        output['SubCategories'] = " | ".join(
            [subcat.name for subcat in answer.subcategory.all()])
        output['Audiences'] = " | ".join(
            aud.name for aud in answer.audiences.all())
        output['RelatedQuestions'] = " | ".join(
            ['{}'.format(a.id) for a in answer.related_questions.all()])
        output['RelatedResources'] = (
            answer.next_step.title
            if answer.next_step
            else '')
        output_rows.append(output)
    return output_rows


def export_questions(path=None):
    """
    A script for exporting Ask CFPB Answer content
    to a CSV that can be opened easily in Excel.

    Run from within cfgov-refresh with:
    `python cfgov/manage.py runscript export_ask_data`

    CEE staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. So we throw in the towel and encode the CSV
    with windows-1252.

    The script will dump the file to `/tmp/` unless a path argument
    is supplied. A command that passes in path would look like this:
    `python cfgov/manage.py runscript export_ask_data --script-args [PATH]`
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = 'ask-cfpb-{}.csv'.format(timestamp)
    if path is None:
        path = '/tmp'
    file_path = '{}/{}'.format(path, slug).replace('//', '/')
    with open(file_path, 'w') as f:
        writer = csvkit.UnicodeWriter(f, encoding='windows-1252')
        writer.writerow(HEADINGS)
        for row in assemble_output():
            writer.writerow(
                [row[key] for key in HEADINGS])


def run(*args):
    if args:
        export_questions(file_path=args[0])
    else:
        export_questions()
