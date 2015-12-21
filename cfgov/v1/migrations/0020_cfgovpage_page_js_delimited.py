# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0019_auto_20151221_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='page_js_delimited',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
