# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_share_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    try:
        v1_content_type = ContentType.objects.get(app_label="v1", model="cfgovpage")
    except ContentType.DoesNotExist:
        v1_content_type = ContentType.objects.create(app_label="v1", model="cfgovpage")

    # Create share permission
    share_permission = Permission.objects.create(
        content_type=v1_content_type,
        codename='share_page',
        name='Can share pages'
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.all():
        group.permissions.add(share_permission)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_share_permissions),
    ]
