# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0050_auto_20160218_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractfilterpage',
            name='preview_link_url',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
