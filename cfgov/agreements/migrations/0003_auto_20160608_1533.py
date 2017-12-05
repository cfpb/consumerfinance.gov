# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0002_auto_20160524_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='file_name',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='uri',
            field=models.URLField(max_length=500),
        ),
    ]
