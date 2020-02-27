from __future__ import unicode_literals

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data, set_stream_data, strip_tags


def escape_heading(heading):
    return heading.lower().replace(' ', '_')


def update_sidefoot():
    draft_pages = []
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue
        if page.has_unpublished_changes:
            draft_pages.append(url)
            continue

        stream_data = get_stream_data(page, 'sidefoot')
        new_data = []
        for field in stream_data:
            if field['type'] == 'related_metadata':
                print(url)
                eam = {'type': 'enforcement_action_metadata', 'value': {}}
                fieldVal = field['value']
                val = eam['value']
                val['slug'] = fieldVal['slug']
                for block in fieldVal['content']:
                    if block['type'] == 'categories':
                        val['categories'] = block['value']['show_categories']
                    elif block['type'] == 'topics':
                        val['topics'] = block['value']['show_topics']
                    elif block['type'] == 'date':
                        val['date_filed'] = block['value']['date']
                    else:
                        heading = escape_heading(block['value']['heading'])
                        blob = strip_tags(block['value']['blob'])
                        print(heading)
                        print(blob)
                        if not blob:
                            print('No', heading, 'for', url)
                        val[heading] = blob
                new_data.append(eam)
            else:
                new_data.append(field)
        set_stream_data(page.specific, 'sidefoot', new_data)

    if len(draft_pages) > 0:
        print('Skipped the following draft pages:', ' '.join(draft_pages))
    else:
        print('No draft pages found, all valid enforcement pages updated')


def run():
    update_sidefoot()
