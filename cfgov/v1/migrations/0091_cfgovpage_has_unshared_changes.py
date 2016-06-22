# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations, models


def update_page_statuses(apps, schema_editor):
    CFGOVPage = apps.get_model('v1.CFGOVPage')
    PageRevision = apps.get_model('wagtailcore.PageRevision')

    for page in CFGOVPage.objects.all():
        revisions = PageRevision.objects.filter(page=page.id).order_by('-created_at', '-id')
        latest_revision = revisions.first()
        latest_content = json.loads(latest_revision.content_json)
        if not latest_content['shared']:
            page.has_unshared_changes = True
        for revision in revisions:
            content = json.loads(revision.content_json)
            if content['live']:
                page.live = True
            if content['shared']:
                page.shared = True
        page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0089_auto_20160607_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='has_unshared_changes',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(update_page_statuses)
    ]
