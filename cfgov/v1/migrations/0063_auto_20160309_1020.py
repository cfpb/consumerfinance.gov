# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0062_auto_20160311_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='live_stream_date',
            field=models.DateTimeField(null=True, verbose_name=b'Go Live Date', blank=True),
        ),
    ]
