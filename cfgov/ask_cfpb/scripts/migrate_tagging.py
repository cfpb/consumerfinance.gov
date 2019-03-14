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
    'Credit cards': 3,
    'Credit reports and scores': 4,
    'Debt collection': 5,
    'Fraud and scams': 7,
    'Money transfers': 8,
    'Mortgages': 9,
    'Payday loans': 10,
    'Prepaid cards': 11,
    'Reverse mortgages': 12,
    'Student loans': 13,
}
CATEGORY_IDS = {
    'Basics': 1,
    'Know your rights': 2,
    'How-to': 3,
    'Key terms': 4,
    'Common issues': 5,
}


# header = (
#     "ask_id,url,Topic,SubCategories,Audiences,"
#     "PrimaryCategoryTag,CategoryTag2,CategoryTag3,CategoryTag4,"
#     "PrimaryTopicTag,TopicTag2,TopicTag3,TopicTag4,TopicTag5")
def run():
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
                ]
            output = transform_csv(data, portal_name)
            if not output:
                print("No output produced")
                return
            output_json(output, slug)
            print("Output {}.json".format(slug))
        apply_tags(output)
        print("Tag migrations took {}".format(
            datetime.datetime.now() - starter))


def apply_tags(data):
    """Apply tagging values to answer pages."""
    category_map = {obj.pk: obj for obj in PortalCategory.objects.all()}
    migration_user_pk = os.getenv('MIGRATION_USER_PK')
    user = User.objects.filter(id=migration_user_pk).first()  # default is None
    for entry in data:
        pages = AnswerPage.objects.filter(
            answer_base__pk=entry.get('ask_id'))
        for page in pages:
            initial_status = page.status_string
            page.get_latest_revision().publish()
            portal_ids = entry.get('portal_ids')
            category_ids = entry.get('see_all_ids')
            for portal_id in portal_ids:
                topic = PortalTopic.objects.get(pk=portal_id)
                page.portal_topic.add(topic)
            for category_id in category_ids:
                category_object = category_map.get(category_id)
                if category_object:
                    page.portal_category.add(category_object)
            page.save_revision(user=user).publish()
            if initial_status == 'draft':
                page.unpublish()


def output_json(data, slug):
    with open("{}/{}.json".format(FIXTURE_DIR, slug), 'w') as f:
        f.write(json.dumps(data, indent=4))


def transform_csv(dict_rows, portal):
    """Turn a CE spreadsheet into a json mapping file."""
    output = []
    portal_pk = PORTAL_IDS.get(portal)
    for row in dict_rows:
        categories = [
            tag.strip() for tag in [
                row['PrimaryCategoryTag'],
                row['CategoryTag2'],
                row['CategoryTag3'],
                row['CategoryTag4']]
            if tag.strip()]
        category_pks = [CATEGORY_IDS.get(tag) for tag in categories
                        if CATEGORY_IDS.get(tag)]
        entry = {
            'ask_id': row.get('ask_id'),
            'portal_ids': [portal_pk],
            'see_all_ids': category_pks,
        }
        output.append(entry)
    return output
