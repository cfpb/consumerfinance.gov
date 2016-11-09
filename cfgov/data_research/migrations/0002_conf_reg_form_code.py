# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='codes',
        ),
        migrations.AddField(
            model_name='conferenceregistration',
            name='code',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
