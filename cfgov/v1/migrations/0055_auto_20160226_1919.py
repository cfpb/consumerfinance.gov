# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0054_auto_20160229_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='browsefilterablepage',
            name='secondary_nav_order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='browsepage',
            name='secondary_nav_order',
            field=models.IntegerField(default=1),
        ),
    ]
