import json
from v1.models import DocumentDetailPage
from wagtail.wagtailcore.models import PageRevision

def run():
    for page in DocumentDetailPage.objects.all():
        for i, child in enumerate(page.header.stream_data):
            if child['type'] == 'item_introduction':
                if 'admin-adj-process' in child['value']['category']:
                    page.header.stream_data[i]['value']['category'] = 'admin-filing'
                    page.save()
        revisions = PageRevision.objects.filter(page=page).order_by('-id')
        latest_revision = revisions.first()
        revisions_to_update = {'shared': None, 'live': None}
        for attr in revisions_to_update.keys():
            for revision in revisions:
                content = json.loads(revision.content_json)
                if content[attr]:
                    revisions_to_update[attr] = revision
        revisions_to_update.update({'latest': latest_revision})
        page_content = json.loads(latest_revision.content_json)
        header = json.loads(page_content['header'])
        for i, child in enumerate(header):
            if child['type'] == 'item_introduction':
                if 'admin-adj-process' in child['value']['category']:
                    header[i]['value']['category'] = 'admin-filing'
        page_content['header'] = json.dumps(header)
        for i, category in enumerate(page_content['categories']):
            if 'admin-adj-process' in category['name']:
                page_content['categories'][i]['name']  = 'admin-filing'
        content = json.dumps(page_content)
        for revision in revisions_to_update.values():
            if revision:
                revision.content_json = content
                revision.save()
