from __future__ import unicode_literals

from v1.models import DocumentDetailPage, BrowseFilterablePage
from v1.models.learn_page import EnforcementActionPage
from v1.models import CFGOVPageCategory
from v1.util.migrations import get_stream_data, set_stream_data, strip_tags

import json


def get_metadata_value(item, variable):
    return strip_tags(item['value']['blob']) or None


def update_sidefoot():
    enforcement_actions = BrowseFilterablePage.objects.get(pk=1327)

    errors = []
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not url or 'policy-compliance/enforcement/actions' not in url:
            continue
        if 'enforcement-action-definitions' in url:
            continue


        keys = vars(page)

        old_categories = page.categories.all()
        if not len(old_categories):
            errors.append(f'No assigned categories for {url}')
            continue

        category = CFGOVPageCategory(name=old_categories[0].name)

        tags = page.tags.all()
        sidefoot = get_stream_data(page, 'sidefoot')
        sidefoot_fields = []
        continue_outer_loop = False

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
                            court = get_metadata_value(item, heading)
                        elif heading in ['Institution type', 'Institution']:
                            institution_type = get_metadata_value(item, heading)
                        elif heading == 'Status':
                            status = get_metadata_value(item, heading)
                        elif heading.lower() in [
                            'docket number',
                            'case number',
             #               'case numbers',
                            'file number',
              #              'file numbers',
                            'civil action number'
                        ]:
                            docket_number = item['value']['blob']
                        elif heading == 'Date filed':
                            date_filed = item['value']['date']
                        elif (heading == 'Category' or heading == 'Topics' or heading == 'Last updated'):
                            continue
                        else:
                            errors.append(f'Unexpected variable {heading} with value {item["value"]} in {url}')
                    except:
                        errors.append(f'Error accessing {heading} metadata for {url}')
                        continue_outer_loop = True
            else:
                sidefoot_fields.append(field)

        if continue_outer_loop:
            continue
        if not institution_type:
            errors.append(f'Missing Institution type for {url}')
            continue
        if not status:
            errors.append(f'Missing Status for {url}')
            continue
        if not docket_number:
            errors.append(f'Missing Docket number for {url}')
            continue

        page.delete()

        eap = EnforcementActionPage(
            depth = keys['depth'],
            live = keys['live'],
            categories = [category],
            latest_revision_created_at = keys['latest_revision_created_at'],
            slug = keys['slug'],
            seo_title = keys['seo_title'],
            preview_title = keys['preview_title'],
            preview_description = keys['preview_description'],
            title = keys['title'],
            header = keys['header'],
            content = keys['content'],
            sidebar_header = 'Action Details',
            court = court,
            docket_number = docket_number,
            status = status
                .replace('-', ' ')
                .replace('udge', 'udg')
                .title(),
            institution_type = institution_type,
            date_filed = date_filed or keys['date_filed']
        )

        enforcement_actions.add_child(instance=eap)

        eap.tags.add(*tags)
        set_stream_data(eap, 'sidefoot', sidefoot_fields)
        
        rev = eap.save_revision()
        eap.latest_revision_created_at = keys['latest_revision_created_at']
        eap.save()

        if keys['live']:
          rev.publish()

    print('\n')
    for error in errors:
        print(error, '\n')


def run():
    update_sidefoot()
