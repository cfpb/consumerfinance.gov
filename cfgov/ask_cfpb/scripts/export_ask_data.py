from __future__ import unicode_literals

import datetime
import HTMLParser

from django.utils import html

import unicodecsv

from ask_cfpb.models import Answer


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

        if answer.english_page:
            output['URL'] = answer.english_page.url_path.replace(
                '/cfgov', '')
            output['Live'] = answer.english_page.live
            output['Redirect'] = answer.english_page.redirect_to_id
        output['SpanishQuestion'] = answer.question_es.replace('\x81', '')
        output['SpanishAnswer'] = clean_and_strip(
            answer.answer_es).replace('\x81', '')

        if answer.spanish_page:
            output['SpanishURL'] = answer.spanish_page.url_path.replace(
                '/cfgov', '')
            output['SpanishLive'] = answer.spanish_page.live
            output['SpanishRedirect'] = answer.spanish_page.redirect_to_id

        output['Topic'] = (answer.category.first().name
                           if answer.category.all() else '')
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


def export_questions(path='/tmp'):
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
    file_path = '{}/{}'.format(path, slug).replace('//', '/')
    with open(file_path, 'w') as f:
        writer = unicodecsv.writer(f, encoding='windows-1252')
        writer.writerow(HEADINGS)
        for row in assemble_output():
            writer.writerow(
                [row.get(key) for key in HEADINGS])


def run(*args):
    if args:
        export_questions(path=args[0])
    else:
        export_questions()
