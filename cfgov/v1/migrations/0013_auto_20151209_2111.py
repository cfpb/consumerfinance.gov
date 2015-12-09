# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fix_beta_notice(apps, schema_editor):
    Flag = apps.get_model('flags','flag')
    beta_flag = Flag.objects.get(pk='BETA_NOTICE')
    beta_flag.enabled_by_default=True
    beta_flag.save()

class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0012_auto_20151209_2049'),
    ]

    operations = [
            migrations.RunPython(fix_beta_notice)
    ]
