from __future__ import unicode_literals

import datetime

import HTMLParser
from django.utils import html

from paying_for_college.csvkit import csvkit

from ask_cfpb.models import Answer

html_parser = HTMLParser.HTMLParser()

# If Spanish snippets are implemented, add the commented heading and output
HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    # 'SpanishShortAnswer',  # add if snippets are implemented for Spanish
    'SpanishAnswer',
    'URL',
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
        # add the following output if Spanish snippets are implemented
        # output['SpanishShortAnswer'] = clean_and_strip(
        #     answer.snippet_es)
        output['SpanishAnswer'] = clean_and_strip(
            answer.answer_es)
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


def export_questions(excel=True):
    """
    Script for exporting Ask CFPB Answer content to a CSV spreadsheet.

    Since our CEE staffers use Excel, the default export encodes the CSV
    in UTF-16le so Excel will open the file with proper diacritical marks.
    This doubles the file size.

    To get a proper utf-8 CSV, pass `excel=False` to export_quesitons.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    with open('answers_{}.csv'.format(timestamp), 'w') as f:
        if excel:
            writer = csvkit.UnicodeWriter(f, encoding='UTF-16le')
        else:
            writer = csvkit.UnicodeWriter(f)
        writer.writerow(HEADINGS)
        for row in assemble_output():
            writer.writerow([row[key] for key in HEADINGS])


def run():
    export_questions()
