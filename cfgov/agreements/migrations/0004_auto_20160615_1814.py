# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0003_auto_20160608_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuer',
            name='slug',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issuer',
            name='name',
            field=models.TextField(max_length=500),
        ),
    ]
