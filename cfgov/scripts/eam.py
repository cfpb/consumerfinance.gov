from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from v1.models import DocumentDetailPage
from v1.models.learn_page import EnforcementActionPage
from v1.util.migrations import get_stream_data, set_stream_data

import json


def update_sidefoot():
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue

        keys = vars(page)
        
        page.delete()

        eap = EnforcementActionPage.objects.create(
            path = keys['path'],
            depth = keys['depth'],
            latest_revision_created_at = keys['latest_revision_created_at'],
            slug = keys['slug'],
            title = keys['title'],
            header = keys['header'],
            content = keys['content'],
            date_filed = keys['date_filed'],
            sidebar_header = 'sh',
            court = 'c',
            docket_number = '123',
            status = 'Post Order/Post Judgment',
            institution_type = 'Nonbank'
        )


def run():
    update_sidefoot()
