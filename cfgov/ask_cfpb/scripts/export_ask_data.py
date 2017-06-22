from __future__ import unicode_literals

import datetime

import HTMLParser
from django.utils import html

from paying_for_college.csvkit import csvkit

from ask_cfpb.models import Answer

html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'SpanishURL',
    'Topic',
    'SubCategories',
    'Audiences',
    'RelatedQuestions',
    'RelatedResources',
]

SPANISH_HEADINGS = [
    'SpanishAnswer',
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output(spanish_only=False):
    answers = Answer.objects.all()
    output_rows = []
    if spanish_only:
        for answer in answers:
            output = {
                'SpanishAnswer': clean_and_strip(answer.answer_es)
            }
            output_rows.append(output)
        return output_rows
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


def export_questions(spanish_only=False):
    """
    Script for exporting Ask CFPB Answer content to a CSV spreadsheet.

    CEE staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. Generally the only content that has characters
    outside the ascii range is Spanish asnwers, so we export the bulk of the
    data as UTF-8, and Spanish answers as a separate UTF-16le file that our
    versions of Excel will read with proper diacritical marks.
    UTF-16le doubles the file size, which causes performance issues for
    the full data set.

    So passing `--script-args spanish' will output just the Ask IDs
    and Spanish answers in UTF-16le. The default (no script args)
    outputs the full data set, minus Spanish answers, in UTF-8.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    if spanish_only:
        filename = 'spanish_answers_{}.csv'
    else:
        filename = 'answers_{}.csv'
    with open(filename.format(timestamp), 'w') as f:
        if spanish_only:
            writer = csvkit.UnicodeWriter(f, encoding='UTF-16le')
            writer.writerow(SPANISH_HEADINGS)
            for row in assemble_output(spanish_only=True):
                writer.writerow([row[key] for key in SPANISH_HEADINGS])
        else:
            writer = csvkit.UnicodeWriter(f)
            writer.writerow(HEADINGS)
            for row in assemble_output():
                writer.writerow([row[key] for key in HEADINGS])


def run(*args):
    if 'spanish' in args:
        export_questions(spanish_only=True)
    else:
        export_questions()
