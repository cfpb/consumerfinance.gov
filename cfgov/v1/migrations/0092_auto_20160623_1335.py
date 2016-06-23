# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from v1.models import CFGOVPage


def save_live_pages(apps, schema_editor):
    for page in CFGOVPage.objects.live():
        if not page.has_unpublished_changes:
            revision = page.get_latest_revision()
            revision.publish()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0091_auto_20160609_1603'),
    ]

    operations = [
        migrations.RunPython(save_live_pages),
    ]
