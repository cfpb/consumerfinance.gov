# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0059_alj_filterable_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='language',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
    ]
