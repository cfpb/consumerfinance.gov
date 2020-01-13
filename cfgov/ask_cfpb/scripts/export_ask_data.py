from __future__ import unicode_literals

import datetime
from six.moves import html_parser as HTMLParser

from django.http import HttpResponse
from django.utils import html

import unicodecsv

from ask_cfpb.models.pages import AnswerPage


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'PAGE_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'Live',
    'Redirect',
    'PortalTopics',
    'PortalCategories',
    'RelatedQuestions',
    'RelatedResource',
    'Language'
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():

    prefetch_fields = (
        'related_questions',
        'portal_topic__heading',
        'portal_category__heading')
    answer_pages = list(AnswerPage.objects.prefetch_related(
        *prefetch_fields).order_by('language', '-answer_base__id').values(
            'id', 'answer_base__id', 'question', 'short_answer',
            'answer_content', 'url_path', 'live', 'redirect_to_page_id',
            'related_resource__title', 'language', *prefetch_fields))
    output_rows = []
    seen = []

    for page in answer_pages:
        # There are duplicate pages in here
        # because of the ManyToMany fields prefetched:
        if page['id'] in seen:
            continue
        seen.append(page['id'])

        output = {heading: '' for heading in HEADINGS}
        output['ASK_ID'] = page['answer_base__id']
        output['PAGE_ID'] = page['id']
        output['Language'] = page['language']
        output['RelatedResource'] = page['related_resource__title']
        output['Question'] = page['question'].replace('\x81', '')
        answer_streamfield = page['answer_content'].stream_data
        answer_text = list(filter(
            lambda item: item['type'] == 'text', answer_streamfield))
        if answer_text:
            answer = answer_text[0].get('value').get('content')
        else:
            # If no text block is found,
            # there is either a HowTo or FAQ schema block.
            # Both define a description field, so we'll use that here.
            answer_schema = filter(
                lambda item: item['type'] == 'how_to_schema' or
                item['type'] == 'faq_schema', answer_streamfield)
            if answer_schema:
                answer = next(answer_schema).get('value').get('description')

        output['Answer'] = clean_and_strip(answer).replace('\x81', '')
        output['ShortAnswer'] = clean_and_strip(page['short_answer'])
        output['URL'] = page['url_path'].replace('/cfgov', '')
        output['Live'] = page['live']
        output['Redirect'] = page['redirect_to_page_id']

        # Group the ManyToMany fields together:
        related_questions = []
        portal_topics = []
        portal_categories = []
        for p in answer_pages:
            if p['id'] == page['id']:
                if p['related_questions']:
                    related_questions.append(str(p['related_questions']))
                if p['portal_topic__heading']:
                    portal_topics.append(p['portal_topic__heading'])
                if p['portal_category__heading']:
                    portal_categories.append(p['portal_category__heading'])

        # Remove duplicates
        related_questions = list(set(related_questions))
        portal_topics = list(set(portal_topics))
        portal_categories = list(set(portal_categories))

        output['RelatedQuestions'] = " | ".join(related_questions)
        output['PortalTopics'] = " | ".join(portal_topics)
        output['PortalCategories'] = " | ".join(portal_categories)
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
