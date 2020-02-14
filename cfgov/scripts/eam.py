from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from v1.models import DocumentDetailPage, BrowseFilterablePage
from v1.models.learn_page import EnforcementActionPage
from v1.util.migrations import get_stream_data, set_stream_data

import json


def update_sidefoot():
    enforcement_actions = BrowseFilterablePage.objects.get(pk=1327)
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not url or 'policy-compliance/enforcement/actions' not in url:
            continue
        if 'enforcement-action-definitions' in url:
            continue

        keys = vars(page)
        #tags = page.tags.all()

        #keys['sidefoot'])

        page.delete()

        eap = EnforcementActionPage(
            depth = keys['depth'],
            live = keys['live'],
            latest_revision_created_at = keys['latest_revision_created_at'],
            slug = keys['slug'],
            preview_title = keys['preview_title'],
            preview_description = keys['preview_description'],
            title = keys['title'],
            header = keys['header'],
            content = keys['content'],
            #sidefoot = keys['sidefoot'],
            sidebar_header = 'sh',
            court = 'c',
            docket_number = '123',
            status = 'Post Order/Post Judgment',
            institution_type = 'Nonbank',
            date_filed = keys['date_filed']
        )

        enforcement_actions.add_child(instance=eap)
        
        rev = eap.save_revision()
        eap.latest_revision_created_at = keys['latest_revision_created_at']
        eap.save()

        if keys['live']:
          rev.publish()

        break

def run():
    update_sidefoot()
