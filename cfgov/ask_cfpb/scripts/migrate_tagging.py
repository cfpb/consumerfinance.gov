from __future__ import unicode_literals

import csv
import datetime
import json
import os

from django.conf import settings
from django.contrib.auth.models import User

from ask_cfpb.models import AnswerPage
from v1.models import PortalCategory, PortalTopic


PROJECT_ROOT = settings.PROJECT_ROOT
FIXTURE_DIR = "{}/ask_cfpb/fixtures/".format(PROJECT_ROOT)
CSV_BASE_DIR = os.getenv('ASK_CSV_BASE_DIR')
CATEGORY_HEADINGS = [
    'PrimaryCategoryTag',
    'CategoryTag2',
    'CategoryTag3',
    'CategoryTag4'
]
SECONDARY_TOPIC_HEADINGS = [
    'TopicTag2',
    'TopicTag3',
    'TopicTag4',
    'TopicTag5'
]
# mapping of slugs to portal name variations, with the correct variation first
SLUGS = {
    'auto_loans': ['Auto loans'],
    'bank_accounts': ['Bank accounts', 'Bank accounts and services'],
    'credit_cards': ['Credit cards'],
    'credit_reports': ['Credit reports and scores'],
    'debt_collection': ['Debt collection'],
    'fraud_and_scams': [
        'Fraud and scams', 'Frauds and scams', 'Fraud and Scams'],
    'money_transfers': ['Money transfers'],
    'mortgages': ['Mortgages'],
    'payday_loans': ['Payday loans'],
    'prepaid_cards': ['Prepaid cards'],
    'reverse_mortgages': ['Reverse mortgages', 'reverse mortgages'],
    'student_loans': ['Student loans'],
}
PORTAL_IDS = {
    'Auto loans': 1,
    'Bank accounts': 2,
    'Bank accounts and services': 2,
    'Credit cards': 3,
    'Credit reports and scores': 4,
    'Debt collection': 5,
    'Fraud and scams': 7,
    'Frauds and scams': 7,
    'Fraud and Scams': 7,
    'Money transfers': 8,
    'Mortgages': 9,
    'Payday loans': 10,
    'Prepaid cards': 11,
    'Reverse mortgages': 12,
    'reverse mortgages': 12,
    'Student loans': 13,
}
CATEGORY_IDS = {
    'Basics': 1,
    'Know your rights': 2,
    'How-to': 3,
    'Key terms': 4,
    'Common issues': 5,
}
CATEGORY_OBJECTS = {obj.pk: obj for obj in PortalCategory.objects.all()}
TOPIC_OBJECTS = {obj.pk: obj for obj in PortalTopic.objects.all()}
MIGRATION_USER_PK = os.getenv('MIGRATION_USER_PK')
USER = User.objects.filter(id=MIGRATION_USER_PK).first()  # default is None


# header = (
#     "ask_id,url,Topic,SubCategories,Audiences,"
#     "PrimaryCategoryTag,CategoryTag2,CategoryTag3,CategoryTag4,"
#     "PrimaryTopicTag,TopicTag2,TopicTag3,TopicTag4,TopicTag5")
def run(*args):
    starter = datetime.datetime.now()
    for slug in sorted(SLUGS.keys()):
        portal_name = SLUGS[slug][0]
        fixture = "{}{}.json".format(FIXTURE_DIR, slug)
        if os.path.isfile(fixture):
            with open(fixture, 'r') as f:
                output = json.loads(f.read())
        else:
            csv_file = "{}/{}.csv".format(CSV_BASE_DIR, slug)
            if not os.path.isfile(csv_file):
                print("No file found at {}".format(csv_file))
                return
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                data = [
                    row for row in reader
                    if row['PrimaryTopicTag'] in SLUGS[slug]
                    and row['ask_id'].isdigit()
                ]
            output = transform_csv(data, portal_name)
            if not output:
                print("No output produced")
                return
            output_json(output, slug)
            print("Output {}.json".format(slug))
        if args and args[0].isdigit() and AnswerPage.objects.filter(
                redirect_to_page=None,
                answer_base__pk=int(args[0])).exists():
            apply_tags(output, singleton=args[0])
        else:
            apply_tags(output)
    print("Tag migrations took {}".format(
        datetime.datetime.now() - starter))


def update_feedback_default(stream_value):
    new_stream_data = stream_value.stream_data
    new_stream_data[0]['value'].update(
        {'was_it_helpful_text': 'Was this answer helpful to you?'})
    stream_value.stream_data = new_stream_data
    return stream_value


def update_page(page, entry):
    initial_status = page.status_string
    page.user_feedback = update_feedback_default(page.user_feedback)
    primary_topic = entry.get('primary_topic')
    topic_ids = entry.get('topics')
    category_ids = entry.get('categories')
    if len(topic_ids) > 1:
        page.primary_portal_topic = TOPIC_OBJECTS.get(primary_topic)
    for topic_id in topic_ids:
        page.portal_topic.add(TOPIC_OBJECTS.get(topic_id))
    for category_id in category_ids:
        page.portal_category.add(CATEGORY_OBJECTS.get(category_id))
    page.save_revision(user=USER).publish()
    if initial_status == 'draft':
        page.unpublish()


def apply_tags(data, singleton=None):
    """Apply tagging values to answer pages, or to a single Ask ID."""
    if singleton:
        if singleton not in [d['ask_id'] for d in data]:
            return
        pages = AnswerPage.objects.filter(
            redirect_to_page=None,
            answer_base__pk=singleton)
        entry = [d for d in data if d['ask_id'] == singleton][0]
        for page in pages:
            update_page(page, entry)
        return
    for entry in data:
        pages = AnswerPage.objects.filter(
            redirect_to_page=None,
            answer_base__pk=entry.get('ask_id')
        )
        for page in pages:
            update_page(page, entry)


def output_json(data, slug):
    with open("{}/{}.json".format(FIXTURE_DIR, slug), 'w') as f:
        f.write(json.dumps(data, indent=4))


def valid_tags(row, headings, ids):
    return [
        row[heading].strip()
        for heading in headings
        if row[heading].strip()
        and row[heading].strip() in ids
    ]


def transform_csv(dict_rows, portal):
    """Turn a CE spreadsheet into a json mapping file."""
    output = []
    primary_portal_pk = PORTAL_IDS.get(portal)
    for row in dict_rows:
        category_strings = valid_tags(row, CATEGORY_HEADINGS, CATEGORY_IDS)
        category_pks = [CATEGORY_IDS.get(tag) for tag in category_strings]
        topic_strings = valid_tags(row, SECONDARY_TOPIC_HEADINGS, PORTAL_IDS)
        topic_pks = [primary_portal_pk] + [
            PORTAL_IDS.get(topic) for topic in topic_strings
        ]
        entry = {
            'ask_id': row.get('ask_id'),
            'primary_topic': primary_portal_pk,
            'categories': sorted(set(category_pks)),
            'topics': sorted(set(topic_pks)),
        }
        output.append(entry)
    return output
