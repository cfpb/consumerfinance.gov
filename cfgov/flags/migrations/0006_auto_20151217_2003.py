# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_beta_flag(apps,schema_editor):
    Flag=apps.get_model('flags','flag')
    beta_notice = Flag(key='BETA_NOTICE', enabled_by_default=True)
    beta_notice.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0005_flag_enabled_by_default'),
    ]

    operations = [
	migrations.RunPython(add_beta_flag)
    ]
