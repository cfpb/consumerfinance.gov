from __future__ import unicode_literals

import datetime
from six.moves import html_parser as HTMLParser

from django.http import HttpResponse
from django.utils import html

import unicodecsv

from ask_cfpb.models.django import Answer
from ask_cfpb.models.pages import AnswerPage


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'Live',
    'Redirect',
    'SpanishQuestion',
    'SpanishAnswer',
    'SpanishURL',
    'SpanishLive',
    'SpanishRedirect',
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
    prefetch_fields = (
        'category__name',
        'subcategory__name',
        'audiences__name',
        'related_questions',
        'next_step__title')
    answers = list(Answer.objects.prefetch_related(*prefetch_fields).values(
        'id', *prefetch_fields))

    answer_pages = list(AnswerPage.objects.values(
        'language', 'answer_base__id', 'url_path', 'live',
        'redirect_to_id', 'question', 'answer', 'snippet'
    ))

    output_rows = []
    seen = []

    for answer in answers:
        # There are duplicate answer_ids in here
        # because of the ManyToMany fields prefetched:
        if answer['id'] in seen:
            continue
        seen.append(answer['id'])

        output = {heading: '' for heading in HEADINGS}
        output['ASK_ID'] = answer['id']
        output['RelatedResources'] = answer['next_step__title']
        output['Topic'] = answer['category__name']

        for page in answer_pages:
            if page['answer_base__id'] == answer['id']:
                if page['language'] == 'en':
                    output['Question'] = page['question']
                    output['Answer'] = clean_and_strip(page['answer'])
                    output['ShortAnswer'] = clean_and_strip(page['snippet'])
                    output['URL'] = page['url_path'].replace('/cfgov', '')
                    output['Live'] = page['live']
                    output['Redirect'] = page['redirect_to_id']
                elif page['language'] == 'es':
                    output['SpanishQuestion'] = page['question'].replace(
                        '\x81', '')
                    output['SpanishAnswer'] = clean_and_strip(
                        page['answer']).replace('\x81', '')
                    output['SpanishURL'] = page['url_path'].replace(
                        '/cfgov', '')
                    output['SpanishLive'] = page['live']
                    output['SpanishRedirect'] = page['redirect_to_id']

        # Group the ManyToMany fields together:
        audiences = []
        related_questions = []
        subcategories = []
        for a in answers:
            if a['id'] == answer['id']:
                if a['audiences__name']:
                    audiences.append(a['audiences__name'])
                if a['related_questions']:
                    related_questions.append(str(a['related_questions']))
                if a['subcategory__name']:
                    subcategories.append(a['subcategory__name'])

        # Remove duplicates
        audiences = list(set(audiences))
        related_questions = list(set(related_questions))
        subcategories = list(set(subcategories))

        output['Audiences'] = " | ".join(audiences)
        output['RelatedQuestions'] = " | ".join(related_questions)
        output['SubCategories'] = " | ".join(subcategories)
        output_rows.append(output)
    return output_rows


def export_questions(path='/tmp', http_response=False):
    """
    A script for exporting Ask CFPB Answer content
    to a CSV that can be opened easily in Excel.

    Run from within cfgov-refresh with:
    `python cfgov/manage.py runscript export_ask_data`

    CEE staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. So we throw in the towel and encode the CSV
    with windows-1252.

    By default, the script will dump the file to `/tmp/`,
    unless a path argument is supplied,
    or http_response is set to True (for downloads via the Wagtail admin).
    A command that passes in path would look like this:
    `python cfgov/manage.py runscript export_ask_data --script-args [PATH]`
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = 'ask-cfpb-{}.csv'.format(timestamp)
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
        export_questions(path=args[0])
    else:
        export_questions()
