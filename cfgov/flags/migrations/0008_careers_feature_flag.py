# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from jobmanager.views import FLAG_NAME


def create_careers_feature_flag(apps, schema_editor):
    Flag = apps.get_model('flags', 'Flag')
    Flag.objects.get_or_create(
        key=FLAG_NAME,
        defaults={'enabled_by_default': True}
    )


class Migration(migrations.Migration):
    dependencies = [
        ('flags', '0007_unique_flag_site'),
    ]

    operations = [
        migrations.RunPython(create_careers_feature_flag)
    ]
