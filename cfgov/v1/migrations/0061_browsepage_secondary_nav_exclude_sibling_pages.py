# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0060_auto_20160310_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='browsepage',
            name='secondary_nav_exclude_sibling_pages',
            field=models.BooleanField(default=False),
        ),
    ]
