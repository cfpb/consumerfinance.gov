# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_prepaid_release_flag(apps, schema_editor):
    Flag = apps.get_model('flags', 'flag')
    prepaid_release = Flag(key='PREPAID_RELEASE', enabled_by_default=False)
    prepaid_release.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0007_unique_flag_site'),
    ]

    operations = [
        migrations.RunPython(add_prepaid_release_flag)
    ]
