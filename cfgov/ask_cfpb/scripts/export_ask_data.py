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
    'ASK_ID'.encode('UTF16'),
    'SpanishURL'.encode('UTF16'),
    'SpanishAnswer'.encode('UTF16'),
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def clean_and_strip_spanish(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(
        unescaped).strip().replace(
        '\t', ' ').replace(
        '\n', ' ').replace(
        '\r', ' ')


def assemble_output(spanish_only=False):
    answers = Answer.objects.all()
    output_rows = []
    if spanish_only:
        for answer in answers:
            output = {
                'ASK_ID'.encode('UTF16'):
                str(answer.id).encode('UTF16'),
                'SpanishURL'.encode('UTF16'): (
                    answer.spanish_page.url_path.replace(
                        '/cfgov', '').encode('UTF16')
                    if answer.spanish_page else ''.encode('UTF16')),
                'SpanishAnswer'.encode('UTF16'): clean_and_strip_spanish(
                    answer.answer_es).encode('UTF16')
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
    A rather ridiculous script for exporting Ask CFPB Answer content.

    Run from within cfgov-refresh with:
    `python cfgov/manage.py runscript export_ask_data`

    CEE staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. Generally the only Ask content that has characters
    outside the ascii range is Spanish asnwers, so we export the bulk of the
    data as UTF-8, and Spanish answers as a separate UTF-16 file that our
    versions of Excel will open with proper diacritical marks.
    UTF-16 doubles the file size, which can causes Excel performance issues
    for the full data set. UTF-16 also plays hob with delimiting,
    pushing text to next cells and making a mess.

    So passing `--script-args spanish` will output just the Ask IDs, URLs,
    and Spanish answers in UTF-16 to a well-behaved tab-separated file.
    The default (no script args) outputs the full data set to CSV,
    minus Spanish answers, in UTF-8.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    if spanish_only:
        filename = 'spanish_answers_{}.tsv'
    else:
        filename = 'answers_{}.csv'
    with open(filename.format(timestamp), 'w') as f:
        if spanish_only:
            f.write(
                "\t".encode('UTF16').join(
                    SPANISH_HEADINGS) + '\n'.encode('UTF16'))
            for row in assemble_output(spanish_only=True):
                f.write("\t".encode('UTF16').join(
                    [row[key] for key
                     in SPANISH_HEADINGS]) + '\n'.encode('UTF16'))
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
