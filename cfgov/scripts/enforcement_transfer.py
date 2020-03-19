from __future__ import unicode_literals

from html.parser import HTMLParser
from unicodedata import normalize

from v1.models import BrowseFilterablePage, DocumentDetailPage
from v1.models.learn_page import (
    EnforcementActionDocket, EnforcementActionPage, EnforcementActionStatus
)
from v1.util.migrations import get_stream_data, set_stream_data


ENFORCEMENT_PARENT_ID = 1327

STATUS_OPTIONS = [
    'Post Order/Post Judgment',
    'Expired/Terminated/Dismissed',
    'Pending Litigation'
]


class TagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    tag_stripper = TagStripper()
    tag_stripper.feed(html)
    stripped = tag_stripper.get_data()

    try:
        data = stripped.decode('utf-8')
    except (UnicodeEncodeError, AttributeError):
        data = stripped

    return normalize('NFKC', data).strip()


def clean_status(s):
    return s.replace('-', ' ').replace('udge', 'udg').title()


def get_metadata_value(item):
    return strip_tags(item['value']['blob']) or None


def transfer_page(page, parent, errors):
    url = page.get_url()

    if not url or 'policy-compliance/enforcement/actions' not in url:
        return

    keys = vars(page)

    old_categories = page.categories.all()

    if not len(old_categories):
        return errors.append(f'No assigned categories for {url}')

    tags = page.tags.all()
    sidefoot = get_stream_data(page, 'sidefoot')
    sidefoot_fields = []

    court = ''
    docket_number = None
    status = None
    institution_type = None
    date_filed = None

    for field in sidefoot:
        if field['type'] == 'related_metadata':
            metadata = field['value']['content']
            for item in metadata:
                heading = item['value']['heading']

                try:
                    if heading == 'Court':
                        court = get_metadata_value(item)
                    elif heading in ['Institution type', 'Institution']:
                        institution_type = get_metadata_value(item)
                    elif heading == 'Status':
                        listed_status = clean_status(
                            get_metadata_value(item)
                        )
                        if listed_status not in STATUS_OPTIONS:
                            status = STATUS_OPTIONS[0]
                        else:
                            status = listed_status
                    elif heading.lower() in [
                        'docket number',
                        'case number',
                        'case numbers',
                        'file number',
                        'file numbers',
                        'civil action number'
                    ]:
                        docket_number = get_metadata_value(item)
                    elif heading == 'Date filed':
                        date_filed = item['value']['date']
                    elif (
                        heading == 'Category' or
                        heading == 'Topics' or
                        heading == 'Last updated'
                    ):
                        continue
                except Exception:
                    return errors.append(
                        f'Error accessing {heading} metadata for {url}'
                    )
        else:
            sidefoot_fields.append(field)

    if not institution_type:
        return errors.append(f'Missing Institution type for {url}')
    if not status:
        return errors.append(f'Missing Status for {url}')
    if not docket_number:
        return errors.append(f'Missing Docket number for {url}')

    statuses = [EnforcementActionStatus(status=status)]
    docket_numbers = [EnforcementActionDocket(docket_number=docket_number)]

    page.delete()

    eap = EnforcementActionPage(
        depth=keys['depth'],
        live=keys['live'],
        categories=old_categories,
        latest_revision_created_at=keys['latest_revision_created_at'],
        slug=keys['slug'],
        seo_title=keys['seo_title'],
        preview_title=keys['preview_title'],
        preview_description=keys['preview_description'],
        title=keys['title'],
        header=keys['header'],
        content=keys['content'],
        sidebar_header='Action Details',
        court=court,
        docket_numbers=docket_numbers,
        statuses=statuses,
        institution_type=institution_type,
        date_filed=date_filed or keys['date_filed']
    )

    parent.add_child(instance=eap)

    eap.tags.add(*tags)
    set_stream_data(eap, 'sidefoot', sidefoot_fields)

    rev = eap.save_revision()
    eap.latest_revision_created_at = keys['latest_revision_created_at']
    eap.save()

    if keys['live']:
        rev.publish()


def transfer_all_pages():
    enforcement_actions = BrowseFilterablePage.objects.get(
        pk=ENFORCEMENT_PARENT_ID
    )
    errors = []

    for page in DocumentDetailPage.objects.all():
        transfer_page(page, enforcement_actions, errors)

    print('\n')
    if not len(errors):
        print('Transfer completed. No unexpected data encountered.')
    else:
        for error in errors:
            print(error, '\n')


def run():
    transfer_all_pages()
