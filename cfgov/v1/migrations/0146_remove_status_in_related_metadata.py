# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations, models

from v1.util.migrations import migrate_page_types_and_fields


logger = logging.getLogger(__name__)


def remove_status_in_related_metadata(page_or_revision, data):
    """ Removes "Status" heading and blob from related metadata blocks. """
    content = data['content']
    filtered_content = [
        block for block in content
        if block['type'] == 'text' and  block['value']['heading'] != 'Status'
    ]
    data['content'] = filtered_content
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'DocumentDetailPage', 'sidefoot', 'related_metadata'),
    ]
    migrate_page_types_and_fields(
        apps,
        page_types_and_fields,
        remove_status_in_related_metadata
    )


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0145_add_notification_molecule'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            migrations.RunPython.noop
        )
    ]
