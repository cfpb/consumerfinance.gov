from __future__ import unicode_literals

import datetime
import HTMLParser

from django.utils import html

from knowledgebase.models import Question
from paying_for_college.csvkit import csvkit


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'Status',
    'Topic',
    'SubCategories',
    'Audiences',
    'RelatedQuestions',
    'UpsellItems',
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():
    english_questions = Question.objects.exclude(englishanswer=None)
    output_rows = []
    for q in english_questions:
        output = {heading: '' for heading in HEADINGS}
        output['ASK_ID'] = q.id
        output['Question'] = q.title
        output['Answer'] = clean_and_strip(
            q.englishanswer.answer)
        output['ShortAnswer'] = clean_and_strip(
            q.englishanswer.one_sentence_answer)
        output['URL'] = q.englishanswer.get_absolute_url()
        output['Status'] = q.englishanswer.workflow_state
        output['Topic'] = q.question_category.filter(parent=None).first().name
        output['SubCategories'] = " | ".join(
            [qc.name for qc in q.question_category.exclude(parent=None)])
        output['Audiences'] = " | ".join(a.name for a in q.audiences.all())
        output['RelatedQuestions'] = " | ".join(
            [question.__repr__() for question in q.related_questions.all()])
        output['UpsellItems'] = (
            q.englishanswer.upsellitem.title
            if q.englishanswer.upsellitem
            else '')
        output_rows.append(output)
    return output_rows


def export_questions():
    """
    Script for exporting original knowledgebase English answers
    to a spreadsheet.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    with open('questions_{}.csv'.format(timestamp), 'w') as f:
        writer = csvkit.writer(f)
        writer.writerow(HEADINGS)
        for row in assemble_output():
            writer.writerow([row[key] for key in HEADINGS])


def run():
    export_questions()
