# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_beta_flag(apps,schema_editor):
    Flag=apps.get_model('flags','flag')
    beta_notice = Flag(key='BETA_NOTICE')
    beta_notice.save()

class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0011_auto_20151207_1725'),
    ]

    operations = [
            migrations.RunPython(add_beta_flag)
    ]
