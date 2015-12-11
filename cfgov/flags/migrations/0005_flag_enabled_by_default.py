# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fix_beta_notice(apps, schema_editor):
    Flag = apps.get_model('flags','flag')

class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0004_remove_flag_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='enabled_by_default',
            field=models.BooleanField(default=False),
        ),

    ]
