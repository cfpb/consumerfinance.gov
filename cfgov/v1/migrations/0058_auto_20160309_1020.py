# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0057_auto_20160304_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='live_stream_date',
            field=models.DateTimeField(null=True, verbose_name=b'Go Live Date', blank=True),
        ),
    ]
